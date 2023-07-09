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

    # Create the black outline
    cv2.putText(frame, text, (text_x - 1, text_y), font, font_scale, (0, 0, 0), font_thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x + 1, text_y), font, font_scale, (0, 0, 0), font_thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y - 1), font, font_scale, (0, 0, 0), font_thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, (text_x, text_y + 1), font, font_scale, (0, 0, 0), font_thickness + 2, cv2.LINE_AA)

    # Create the white text
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Combine the shadow and frame images with increased opacity
    alpha = 0.9  # Increase the alpha value for a more opaque shadow
    frame = cv2.addWeighted(frame, 1, shadow_img, alpha, 0)

    return frame
