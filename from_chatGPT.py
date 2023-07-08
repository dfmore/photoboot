import cv2
import win32print
import win32con
from datetime import datetime

# Set the desired video capture dimensions
width = 1280
height = 720

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
    # Get the default printer name
    default_printer = win32print.GetDefaultPrinter()

    # Open the printer
    printer_handle = win32print.OpenPrinter(default_printer)

    try:
        # Get the printer properties
        properties = win32print.GetPrinter(printer_handle, 2)

        # Check if the printer supports RAW printing
        if properties['pDevMode'].Specs[0] & win32con.DM_COPIES == 0:
            raise ValueError("The printer does not support RAW printing.")

        # Start the printing job
        win32print.StartDocPrinter(printer_handle, 1, (image_path, None, "RAW"))

        # Open the image file
        file = open(image_path, "rb")
        try:
            # Send the image to the printer
            win32print.StartPagePrinter(printer_handle)
            win32print.WritePrinter(printer_handle, file.read())
            win32print.EndPagePrinter(printer_handle)
        finally:
            # Close the image file
            file.close()

        # End the printing job
        win32print.EndDocPrinter(printer_handle)

    finally:
        # Close the printer
        win32print.ClosePrinter(printer_handle)

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
