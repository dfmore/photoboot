import sys
import cv2
import os
from datetime import datetime
import numpy as np
import time
import pygame
import pygame_gui


# Constants
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
WINDOW_IMAGE_SIZE = (800, 800)
COUNTDOWN_DURATION = 3
SOUND_FILE = 'camera-13695.wav'
CARD_FRAME_PATH = 'frame.png'
FOLDER_PATH = 'G:/My Drive/Memories/[2023] Arthur & Charlie 4yo bday'

def logo():
    return ('''
    ███████╗  █████╗ ███╗   ██╗███████╗        ██████╗ ██╗  ██╗ ██████╗ ████████╗ ██████╗ ██████╗  ██████╗  ██████╗ ████████╗██╗  ██╗
    ██╔══██╗██╔══██╗████╗  ██║██╔════╝        ██╔══██╗██║  ██║██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██║  ██║
    ██║  ██║███████║██╔██╗ ██║███████╗        ██████╔╝███████║██║   ██║   ██║   ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   ███████║
    ██║  ██║██╔══██║██║╚██╗██║╚════██║        ██╔═══╝ ██╔══██║██║   ██║   ██║   ██║   ██║██╔══██╗██║   ██║██║   ██║   ██║   ██╔══██║
    ███████╔╝██║  ██║██║ ╚████║███████║        ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝   ██║   ██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝        ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝
    ''')

def capture_image(frame):
    frame = cv2.flip(frame, 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H%M")
    filename = f"captured_image_{timestamp}.jpg"

    os.makedirs(FOLDER_PATH, exist_ok=True)

    file_path = os.path.join(FOLDER_PATH, filename)
    cv2.imwrite(file_path, frame)

    card_frame = cv2.imread(CARD_FRAME_PATH)

    if card_frame is not None:
        card_frame = cv2.resize(card_frame, (frame.shape[1], frame.shape[0]))

        blended_image = cv2.addWeighted(frame, 1, card_frame, 0.8, 0)

        text = "Arthur & Charlie Birthday Party 2023"
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        font_scale = 3
        font_thickness = 5
        text_color = (255, 255, 255)
        outline_color = (0, 0, 0)

        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

        text_x = int((frame.shape[1] - text_width) / 2)
        text_y = int(frame.shape[0] / 2) + 450

        thickness = font_thickness + 2
        cv2.putText(blended_image, text, (text_x - 3, text_y), font, font_scale, outline_color, thickness, cv2.LINE_AA)
        cv2.putText(blended_image, text, (text_x + 3, text_y), font, font_scale, outline_color, thickness, cv2.LINE_AA)
        cv2.putText(blended_image, text, (text_x, text_y - 3), font, font_scale, outline_color, thickness, cv2.LINE_AA)
        cv2.putText(blended_image, text, (text_x, text_y + 3), font, font_scale, outline_color, thickness, cv2.LINE_AA)

        cv2.putText(blended_image, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        final_file_path = os.path.join(FOLDER_PATH, f"final_{filename}")
        cv2.imwrite(final_file_path, blended_image)

        return final_file_path

    return file_path


def draw_timer(frame, seconds):
    height, width, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 10
    font_thickness = 20
    shadow_offset = 5
    text = str(seconds)
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = int((width - text_width) / 2)
    text_y = int((height + text_height) / 2)
    shadow_img = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(shadow_img, text, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale, (0, 0, 0),
                font_thickness, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x - 3, text_y), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x + 3, text_y), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y - 3), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y + 3), font, font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
    alpha = 0.9
    frame = cv2.addWeighted(frame, 1, shadow_img, alpha, 0)
    return frame


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Dan's PhotoBooth")
    gui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
    capture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),
                                                  text='Capture',
                                                  manager=gui_manager)
    print_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 50)),
                                                text='Print',
                                                manager=gui_manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 250), (100, 50)),
                                               text='Exit',
                                               manager=gui_manager)
    image_rect = pygame.Rect((300, 0), WINDOW_IMAGE_SIZE)
    image_element = pygame_gui.elements.UIImage(image_rect, pygame.Surface(WINDOW_IMAGE_SIZE), manager=gui_manager)

    # Initialize webcam capture with desired dimensions
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set desired width
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set desired height

    capturing = False
    countdown = COUNTDOWN_DURATION
    last_captured_image = None

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
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
                    elif event.ui_element == exit_button:
                        video_capture.release()
                        pygame.quit()
                        cv2.destroyAllWindows()
                        sys.exit(0)

            gui_manager.process_events(event)

        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)

        if capturing:
            if countdown > 0:
                frame = draw_timer(frame, countdown)
                cv2.imshow("Webcam", frame)
                cv2.waitKey(1000)
                countdown -= 1
            else:
                pygame.mixer.init()
                sound = pygame.mixer.Sound(SOUND_FILE)
                sound.play()

                image_path = capture_image(frame)
                cv2.imshow("Captured Image", frame)

                last_captured_image = image_path
                captured_image = pygame.image.load(last_captured_image)
                image_width, image_height = captured_image.get_size()
                max_width = WINDOW_IMAGE_SIZE[0]
                max_height = WINDOW_IMAGE_SIZE[1]
                aspect_ratio = image_width / image_height

                if aspect_ratio > 1:
                    resized_width = max_width
                    resized_height = int(resized_width / aspect_ratio)
                else:
                    resized_height = max_height
                    resized_width = int(resized_height * aspect_ratio)

                resized_image = pygame.transform.smoothscale(captured_image, (resized_width, resized_height))
                image_surface = pygame.Surface((max_width, max_height))
                image_surface.fill((0, 0, 0))
                image_rect = resized_image.get_rect(center=image_surface.get_rect().center)
                image_surface.blit(resized_image, image_rect)
                image_element.set_image(image_surface)

                cv2.destroyWindow("Captured Image")
                capturing = False
                countdown = COUNTDOWN_DURATION

        else:
            cv2.imshow("Webcam", frame)

        gui_manager.update(time_delta)
        gui_manager.draw_ui(window_surface)
        pygame.display.update()

if __name__ == "__main__":
    main()
