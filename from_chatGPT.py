import cv2
import ctypes
import os
from datetime import datetime
import numpy as np
from pathlib import Path
import win32com.client
import tkinter as tk
from tkinter import ttk

# Function to get available cameras
def get_cameras():
    camera_indices = []
    for index in range(10):  # Just a large number in case you have many cameras connected
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            camera_indices.append(index)
            cap.release()
    return camera_indices

    # Create a WMI object
    wmi = win32com.client.GetObject ("winmgmts:")

    # Get a list of all cameras using WMI
    cameras = wmi.InstancesOf ("Win32_PnPEntity")
    
    camera_names = []
    camera_ids = []

    # Iterate through all cameras
    for camera in cameras:
        # Check if the device is a camera
        if "webcam" in camera.Name.lower() or "camera" in camera.Name.lower():
            # Add the camera name and ID to the respective lists
            camera_names.append(camera.Name)
            camera_ids.append(int(camera.DeviceID.replace('Video', '')))

    return camera_ids, camera_names

# Function to prompt user to select camera
def prompt_camera_selection(camera_indices):
    # Create a root window
    root = tk.Tk()
    root.title("Camera Selection")

    # Create a variable to store the selected index
    selected_index = tk.StringVar()

    # Create a Combobox with the list of available camera indices
    combo = ttk.Combobox(root, textvariable=selected_index)
    combo['values'] = camera_indices
    if camera_indices:
        combo.current(0)  # Set the first camera as default
    combo.pack(pady=20)

    # Function to call when the confirm button is clicked
    def confirm():
        # Check if the selected index is valid
        try:
            index = int(selected_index.get())
            if index not in camera_indices:
                print("Invalid camera selected. Please select again.")
            else:
                root.quit()
        except ValueError:
            print("Invalid camera selected. Please select again.")

    # Create a confirm button
    btn = tk.Button(root, text="Confirm", command=confirm)
    btn.pack()

    # Run the GUI loop
    root.mainloop()
    root.destroy()

    # Return the selected camera index
    try:
        return int(selected_index.get())
    except ValueError:
        return None
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Generate a string of available camera indices
    camera_str = ', '.join(str(idx) for idx in camera_indices)

    # Show a dialog asking the user to select a camera
    dialog = simpledialog.askstring("Camera Selection", f"Select Camera ({camera_str}):")

    try:
        selected_index = int(dialog)
        if selected_index not in camera_indices:
            print(f"Invalid camera selected. Available cameras are: {camera_str}")
            return None
        return selected_index
    except (ValueError, TypeError):
        print(f"Invalid input. Available cameras are: {camera_str}")
        return None

    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Show a dialog asking the user to select a camera
    dialog = simpledialog.askstring("Camera Selection", "Select Camera:", initialvalue=camera_names[0])

    # Check if the user-selected camera is valid
    if dialog not in camera_names:
        print(f"Invalid camera selected. Available cameras are: {camera_names}")
        return None

    # Return the index of the selected camera
    return camera_names.index(dialog)

# Function to capture and save an image
def capture_image(frame):
    # Mirror the image horizontally
    frame = cv2.flip(frame, 1)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # Generate the filename with timestamp
    filename = f"captured_image_{timestamp}.jpg"

    # Create the folder on the user's desktop
    folder_name = f"PhotoBooth-{datetime.now().strftime('%Y-%m-%d')}"
    folder_path = Path.home() / "Desktop" / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    # Save the captured frame to the file
    file_path = folder_path / filename
    cv2.imwrite(str(file_path), frame)

    return str(file_path)

# Function to draw the countdown timer on the frame
def draw_timer(frame, seconds):
    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Set the font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 10
    font_thickness = 20
    shadow_offset = 5

    # Calculate the text size
    text = str(seconds)
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Calculate the position to center the text
    text_x = int((width - text_width) / 2)
    text_y = int((height + text_height) / 2)

    # Create a black drop shadow
    shadow_img = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(shadow_img, text, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    # Create the black outline
    cv2.putText(frame, text, (text_x - 3, text_y), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x + 3, text_y), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y - 3), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y + 3), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)

    # Create the white text
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Combine the shadow and frame images with increased opacity
    alpha = 0.9  # Increase the alpha value for a more opaque shadow
    frame = cv2.addWeighted(frame, 1, shadow_img, alpha, 0)

    return frame

# Function to display a dialog box and ask for user input
def prompt_dialog_box(title, message):
    response = ctypes.windll.user32.MessageBoxW(0, message, title, 1)
    return response == 1  # Return True if "Yes" button is clicked

# Main script
def main():
    # Get available cameras
    camera_indices = get_cameras()

    # Prompt user to select camera
    selected_camera_index = prompt_camera_selection(camera_indices)
    if selected_camera_index is None:
        return

    # Set the desired video capture dimensions
    width = 1920
    height = 1080

    # Display the webcam feed
    cap = cv2.VideoCapture(selected_camera_index)

    # Set the video capture dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    capturing = False  # Flag to indicate whether to capture image or not
    countdown = 3  # Countdown duration

    while True:
        ret, frame = cap.read()

        # Mirror the image horizontally
        frame = cv2.flip(frame, 1)

        if capturing:
            if countdown > 0:
                # Draw the countdown timer
                frame = draw_timer(frame, countdown)
                cv2.imshow("Webcam", frame)
                cv2.waitKey(1000)
                countdown -= 1
            else:
                # Capture the image after countdown reaches 0
                image_path = capture_image(frame)
                cv2.imshow("Captured Image", frame)

                # Prompt user if they want to print the captured image
                print_prompt = prompt_dialog_box("Print Confirmation", "Do you want to print the captured image?")
                if print_prompt:
                    try:
                        os.startfile(image_path, "print")
                        print("Printing the captured image:", image_path)
                    except Exception as e:
                        print("Failed to print the image:", str(e))
                else:
                    print("Image capture cancelled.")
                cv2.destroyWindow("Captured Image")
                capturing = False
                countdown = 3
        else:
            cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)
        if key == 27:  # Escape key
            break
        if key == ord("c"):  # "c" key
            capturing = True

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
