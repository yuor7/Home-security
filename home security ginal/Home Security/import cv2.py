import cv2
if hasattr(cv2, 'face'):
    print("cv2.face is available.")
else:
    print("cv2.face is not available. Check installation.")
