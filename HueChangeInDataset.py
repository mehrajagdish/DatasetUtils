import cv2
from glob import glob
from ultralytics import YOLO

# Set your YOLO model path and class names
model_path = "yolov8n.pt"  # Replace with your model path
class_names = ["tennis-ball"]  # Only consider this class

# Initialize YOLO model
model = YOLO(model_path)


# Function to apply pink hue to bounding box area (using OpenCV)
def apply_pink_hue(image, box):
    x_min, y_min, x_max, y_max = box
    cropped_image = image[y_min:y_max, x_min:x_max]  # Crop using OpenCV

    # Convert image to HSV color space (OpenCV style)
    hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

    # Define pink hue range (adjust as needed)
    hue_min, hue_max = 270, 330

    # Shift hue to pink range
    mask = cv2.inRange(hsv_image, (hue_min, 0, 0), (hue_max, 255, 255))
    hsv_image[mask] = (hue_min, 255, 255)

    # Convert back to BGR color space (OpenCV style)
    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Paste the modified image back to the original image
    image[y_min:y_max, x_min:x_max] = rgb_image

    return image


# Get all image paths in directory
image_paths = glob("directory/*.jpg")  # Replace with your directory path

# Loop through each image
for image_path in image_paths:
    # Load image with OpenCV
    image = cv2.imread(image_path)

    # Run object detection
    results = model(image)

    # Loop through each detected object
    for result in results.pandas().xyxy[0]:
        box = [int(x) for x in result[1:5]]  # Extract bounding box coordinates
        class_name = result[0]

        # Check if it's the desired class
        if class_name == "tennis-ball":
            # Apply pink hue
            image = apply_pink_hue(image.copy(), box)

    # Save the modified image with OpenCV
    cv2.imwrite(f"modified_{image_path}", image)

print("Images processed and saved!")
