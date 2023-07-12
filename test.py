import cv2

def get_available_resolutions(src=1, max_frames=10):
    capture = cv2.VideoCapture(src)
    resolutions = set()

    frame_count = 0
    while frame_count < max_frames:
        ret, frame = capture.read()
        if not ret:
            break

        resolution = (frame.shape[1], frame.shape[0])
        resolutions.add(resolution)

        frame_count += 1

    capture.release()
    return list(resolutions)

# Example usage
available_resolutions = get_available_resolutions()
for resolution in available_resolutions:
    print(f"Resolution: {resolution[0]}x{resolution[1]}")


# import cv2
# cap = cv2.VideoCapture(0)
# cap.release()
# cv2.destroyAllWindows()