import cv2
import win32print
from datetime import datetime

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
    
    # Save the captured frame to the file
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

# Main script
def main():
    # Display the webcam feed
    cap = cv2.VideoCapture(0)
    
    # Set the video capture dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    capturing = False  # Flag to indicate whether to capture image or not
    
    while True:
        ret, frame = cap.read()
        
        # Mirror the image horizontally
        frame = cv2.flip(frame, 1)
        
        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)
        
        if key == 27:  # Check for Escape key press
            break
        
        if key == ord("c"):  # Check for "c" key press to capture image
            capturing = True
        
        if capturing:
            capture_image(frame)
            capturing = False
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
