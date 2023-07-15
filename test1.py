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

                # Show the captured image on the screen
                captured_image = cv2.imread(image_path)
                cv2.imshow("Captured Image", captured_image)

                # Prompt user if they want to print the captured image
                print_prompt = get_user_input("Do you want to print the captured image? (y/n) ")
                if print_prompt:
                    try:
                        if sys.platform == 'win32':
                            subprocess.run(['mspaint', '/p', image_path], check=True)
                        else:
                            subprocess.run(['lp', image_path], check=True)
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
