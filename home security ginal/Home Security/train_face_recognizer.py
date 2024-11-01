import cv2
import os

# Define the main dataset directory path (without person1, person2 subfolders)
dataset_dir = r"C:\Users\yuora\OneDrive\Desktop\home security ginal\Home Security\dataset"

# Check if the directory exists
if not os.path.isdir(dataset_dir):
    print(f"Directory not found: {dataset_dir}")
else:
    # Iterate through the files in the dataset directory
    for filename in os.listdir(dataset_dir):
        # Check if the file is an image
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            img_path = os.path.join(dataset_dir, filename)
            img = cv2.imread(img_path)

            if img is not None:
                # Convert the image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Process the gray image (e.g., training, feature extraction, etc.)
                # Example: Show the image (optional)
                # cv2.imshow('Gray Image', gray)
                # cv2.waitKey(0)

                print(f"Processed image: {filename}")
            else:
                print(f"Failed to read image: {filename}")
        else:
            print(f"Skipping non-image file: {filename}")

    # Close all OpenCV windows if opened
    cv2.destroyAllWindows()
