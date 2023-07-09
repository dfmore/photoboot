import cv2
import win32print
from datetime import datetime
import time
import numpy as np

# Set the desired video capture dimensions
width = 1920
height = 1080

# Function to capture and save an image
def capture_image(frame):
    # Mirror the image horizontally
    frame = cv2.flip(frame, 1)
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    
    # Generate the filename with timestamp
    filename = f"captured_image_{timestamp}.jpg"
    
    # Save the captured frame to the file without the countdown number
    cv2.imwrite(filename, frame)

    # Print the captured image
    try:
        print_image(filename)
    except Exception as e:
        print("Failed to print image:", str(e))

# Function to print an image
def print_image(image_path):
    # Open the image file
    file = open(image_path, "rb")
    
    # Get the default printer name
    default_printer = win32print.GetDefaultPrinter()
    
    # Create a print job and send the image to the printer
    win32print.SetDefaultPrinter(default_printer)
    win32print.StartDocPrinter(default_printer, 1, (image_path, None, "RAW"))
    win32print.WritePrinter(default_printer, file.read())
    win32print.EndDocPrinter(default_printer)
    
    # Close the image file
    file.close()

# Function to draw the countdown timer on the frame
def draw_timer(frame, seconds):
    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Set the font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 4
    font_thickness = 6
    shadow_offset = 4

    # Calculate the text size
    text = str(seconds)
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Calculate the position to center the text
    text_x = int((width - text_width) / 2)
    text_y = int((height + text_height) / 2)

    # Create a black drop shadow
    shadow_img = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(shadow_img, text, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    # Create the white text
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Combine the shadow and frame images
    frame = cv2.addWeighted(frame, 1, shadow_img, 0.7, 0)

    return frame

# Main script
def main():
    # Display the webcam feed
    cap = cv2.VideoCapture(0)
    
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
                capture_image(frame)
                capturing = False
                countdown = 3
        else:
            cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)
        
        if key == 27:  # Check for Escape key press
            break
        
        if key == ord("c"):  # Check for "c" key press to initiate countdown
            capturing = True
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
