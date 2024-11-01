import face_recognition
import cv2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Load known faces
dataset_dir = r"C:\Users\yuora\OneDrive\Desktop\home security ginal\Home Security\dataset"  
known_face_encodings = []
known_face_names = []

for filename in os.listdir(dataset_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(dataset_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        
        # Ensure at least one face encoding is detected
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(filename.split('.')[0])  
        else:
            print(f"No face detected in image: {filename}")


cap = cv2.VideoCapture(0)

unknown_faces_detected = False
unknown_face_frame = None
known_face_detected = False

# Set a threshold for face distance
face_match_threshold = 0.6

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Detect faces and get encodings
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Calculate face distances and find the best match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else -1

        if best_match_index != -1 and face_distances[best_match_index] < face_match_threshold:
            name = known_face_names[best_match_index]
            known_face_detected = True  # Set flag for known face detected
        else:
            name = "Unknown"
            unknown_faces_detected = True
            unknown_face_frame = frame

        # Draw rectangle around face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)

    # Press 'q' to quit or break on detection
    if cv2.waitKey(1) & 0xFF == ord('q') or known_face_detected or unknown_faces_detected:
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()

# Email unknown face if detected
if unknown_faces_detected:
    print("Sending email...")

    image_path = os.path.join(os.getcwd(), 'unknown_face.jpg')
    cv2.imwrite(image_path, unknown_face_frame)

    sender_email = "yuorahul77@gmail.com"
    receiver_email = "rmadugula235@gmail.com"
    password = "zuzo knxh siwl vdnm"
    subject = "Unknown face detected"
    body = "An unknown face was detected in the video. Please investigate."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as image_file:
        img_data = image_file.read()
        image = MIMEImage(img_data, name=os.path.basename(image_path))
        msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully with unknown face image.")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("No unknown faces detected.")
