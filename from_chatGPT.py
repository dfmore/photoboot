import cv2
import os
from datetime import datetime
import numpy as np
from threading import Thread
import time
import pygame
import pygame_gui

# Initialize pygame audio mixer
pygame.mixer.init()

# Load the sound file
sound_file = 'C:/Users/Daniel Moreira/Documents/GitHub/photoboot/camera-13695.wav'
sound = pygame.mixer.Sound(sound_file)

# Set the dimensions of the captured image in the window
window_image_size = (800, 800)

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

def logo():
    return ('''
██████╗  █████╗ ███╗   ██╗███████╗        ██████╗ ██╗  ██╗ ██████╗ ████████╗ ██████╗ ██████╗  ██████╗  ██████╗ ████████╗██╗  ██╗
██╔══██╗██╔══██╗████╗  ██║██╔════╝        ██╔══██╗██║  ██║██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║  ██║
██║  ██║███████║██╔██╗ ██║███████╗        ██████╔╝███████║██║   ██║   ██║   ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ███████║
██║  ██║██╔══██║██║╚██╗██║╚════██║        ██╔═══╝ ██╔══██║██║   ██║   ██║   ██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██╔══██║
██████╔╝██║  ██║██║ ╚████║███████║        ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝        ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝
''')

# Function to capture and save an image with birthday card frame
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

    # Load the birthday card frame image
    card_frame_path = 'C:/Users/Daniel Moreira/Documents/GitHub/photoboot/frame.png'  # Replace with the actual path to the birthday card frame image
    card_frame = cv2.imread(card_frame_path)

    if card_frame is not None:
        # Resize the card frame to match the captured image size
        card_frame = cv2.resize(card_frame, (frame.shape[1], frame.shape[0]))

        # Overlay the card frame on the captured image
        blended_image = cv2.addWeighted(frame, 1, card_frame, 0.8, 0)

        # Add text overlay
        text = "Arthur & Charlie Birthday Party 2023"
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # Change the font to FONT_HERSHEY_SCRIPT_SIMPLEX
        font_scale = 3
        font_thickness = 5
        text_color = (255, 255, 255)
        outline_color = (0, 0, 0)  # Black outline color

        # Calculate the text size
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Calculate the position to center the text
        text_x = int((frame.shape[1] - text_width) / 2)
        text_y = int(frame.shape[0] / 2) + 450

        # Draw the black outline
        thickness = font_thickness + 2  # Increase the thickness for the outline
        cv2.putText(
            blended_image,
            text,
            (text_x - 3, text_y),
            font,
            font_scale,
            outline_color,
            thickness,
            cv2.LINE_AA
        )
        cv2.putText(
            blended_image,
            text,
            (text_x + 3, text_y),
            font,
            font_scale,
            outline_color,
            thickness,
            cv2.LINE_AA
        )
        cv2.putText(
            blended_image,
            text,
            (text_x, text_y - 3),
            font,
            font_scale,
            outline_color,
            thickness,
            cv2.LINE_AA
        )
        cv2.putText(
            blended_image,
            text,
            (text_x, text_y + 3),
            font,
            font_scale,
            outline_color,
            thickness,
            cv2.LINE_AA
        )

        # Draw the white text
        cv2.putText(
            blended_image,
            text,
            (text_x, text_y),
            font,
            font_scale,
            text_color,
            font_thickness,
            cv2.LINE_AA
        )

        # Save the final captured image with the birthday card frame
        final_file_path = os.path.join(folder_path, f"final_{filename}")
        cv2.imwrite(final_file_path, blended_image)

        return final_file_path

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

# Main script
def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set the dimensions of the Pygame window
    window_width = 1300
    window_height = 800
    window_surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Dan's PhotoBooth")

    # Create a GUI manager
    gui_manager = pygame_gui.UIManager((window_width, window_height))

    # Create a Pygame GUI button for capturing images
    capture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),
                                                  text='Capture',
                                                  manager=gui_manager)

    # Create a Pygame GUI button for printing the last captured image
    print_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 50)),
                                                text='Print',
                                                manager=gui_manager)

    # Create a Pygame GUI image for displaying the last captured image
    image_rect = pygame.Rect((300, 0), window_image_size)
    image_element = pygame_gui.elements.UIImage(image_rect, pygame.Surface(window_image_size), manager=gui_manager)

    # Display the webcam feed
    print(logo())
    video_stream_widget = VideoStreamWidget(width=1900, height=1080)
    capturing = False  # Flag to indicate whether to capture image or not
    countdown = 3  # Countdown duration
    last_captured_image = None

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_stream_widget.capture.release()
                pygame.quit()
                cv2.destroyAllWindows()
                exit(1)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == capture_button:
                        capturing = True
                    elif event.ui_element == print_button:
                        if last_captured_image:
                            try:
                                os.startfile(last_captured_image, "print")
                                print("Printing the captured image:", last_captured_image)
                            except Exception as e:
                                print("Failed to print the image:", str(e))

            gui_manager.process_events(event)

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

                # Load the last captured image to display in the GUI
                last_captured_image = image_path
                captured_image = pygame.image.load(last_captured_image)

                # Calculate the dimensions of the resized image while maintaining the aspect ratio
                image_width, image_height = captured_image.get_size()
                max_width = window_image_size[0]
                max_height = window_image_size[1]
                aspect_ratio = image_width / image_height

                if aspect_ratio > 1:
                    resized_width = max_width
                    resized_height = int(resized_width / aspect_ratio)
                else:
                    resized_height = max_height
                    resized_width = int(resized_height * aspect_ratio)

                # Resize the captured image to fit within the maximum dimensions while maintaining aspect ratio
                resized_image = pygame.transform.smoothscale(captured_image, (resized_width, resized_height))
                image_surface = pygame.Surface((max_width, max_height))
                image_surface.fill((0, 0, 0))  # Fill with white background
                image_rect = resized_image.get_rect(center=image_surface.get_rect().center)
                image_surface.blit(resized_image, image_rect)
                image_element.set_image(image_surface)

                # Go back to displaying the webcam feed
                cv2.destroyWindow("Captured Image")
                capturing = False
                countdown = 3

        else:
            cv2.imshow("Webcam", frame)

        gui_manager.update(time_delta)

        # Draw the GUI elements on the Pygame surface
        gui_manager.draw_ui(window_surface)

        pygame.display.update()

    video_stream_widget.capture.release()
    pygame.quit()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
