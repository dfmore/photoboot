import cv2
import ctypes
import os
from datetime import datetime
import numpy as np
from pathlib import Path
from threading import Thread
import time
import pygame

# Initialize pygame audio mixer
pygame.mixer.init()

# Load the sound file
sound_file = 'C:/Users/Daniel Moreira/Documents/GitHub/photoboot/camera-13695.wav'
sound = pygame.mixer.Sound(sound_file)

class VideoStreamWidget(object):
    def __init__(self, src=0, width=1920, height=1080):
        print("Start capturing...")
        self.capture = cv2.VideoCapture(src)
        print("Set width " + str(width) + "...")
        setwidth = self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        print("Width set = " + str(setwidth))
        print("Set height " + str(height))
        setheight = self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print("Height set = " + str(setheight))
        self.status, self.frame = self.capture.read()
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):
        # Display frames in the main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)


# Set the desired video capture dimensions
width = 1920
height = 1080

# Function to capture and save an image
def capture_image(frame):
    # Mirror the image horizontally
    frame = cv2.flip(frame, 1)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H%M")

    # Generate the filename with timestamp
    filename = f"captured_image_{timestamp}.jpg"

    # Set the folder path
    folder_path = 'G:/My Drive/Memories/[2023] Arthur & Charlie 4yo bday'

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Save the captured frame to the file without the countdown number
    file_path = os.path.join(folder_path, filename)
    cv2.imwrite(file_path, frame)

    return file_path

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
    # Display the webcam feed
    video_stream_widget = VideoStreamWidget(width=1900, height=1080)
    
    # Wait for a moment to ensure the webcam feed is started
    time.sleep(2)

    capturing = False  # Flag to indicate whether to capture image or not
    countdown = 3  # Countdown duration

    while True:
        frame = video_stream_widget.frame

        # Mirror the image horizontally and rotate
        frame = cv2.flip(frame, 1)

        if capturing:
            if countdown > 0:
                # Draw the countdown timer
                frame = draw_timer(frame, countdown)
                cv2.imshow("Webcam", frame)
                cv2.waitKey(1000)
                countdown -= 1
            else:
                # Play the sound when the countdown reaches 0
                sound.play()

                # Capture the image after the countdown reaches 0
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

                # Go back to displaying the webcam feed
                cv2.destroyWindow("Captured Image")
                capturing = False
                countdown = 3
        else:
            cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)

        if key == 27:  # Check for Escape key press
            break

        if key == ord("c"):  # Check for "c" key press to initiate countdown
            capturing = True

    video_stream_widget.capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
