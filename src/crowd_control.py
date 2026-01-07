from ultralytics import YOLO
import cv2
import pyttsx3
import time
import os
from twilio.rest import Client

# Load YOLO model
model = YOLO('yolov8s.pt')  # You can change to 'yolov8n.pt' for faster but less accurate detection

# Initialize webcam
cap = cv2.VideoCapture(0)

# TTS engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Set voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to default voice

# Secure Twilio credentials from environment variables
twilio_sid = os.getenv('TWILIO_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
destination_phone_number = os.getenv('DESTINATION_PHONE_NUMBER')

if not all([twilio_sid, twilio_auth_token, twilio_phone_number, destination_phone_number]):
    print("❌ Twilio credentials not set. Set them as environment variables.")
    exit(1)

twilio_client = Client(twilio_sid, twilio_auth_token)

# Threshold and cooldown settings
threshold = 3  # Change as needed
last_alert_time = 0
cooldown = 5  # seconds

# Frame loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame from camera.")
        break

    # YOLO detection
    results = model.predict(source=frame, verbose=False)

    # Get class names safely
    names = model.model.names if hasattr(model, "model") else model.names

    # Count detected people
    count = sum(1 for box in results[0].boxes if names[int(box.cls[0])] == 'person')

    # Annotate frame
    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, f'People: {count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display video
    cv2.imshow("Live Crowd Counter", annotated_frame)

    # Voice and SMS alert if above threshold
    current_time = time.time()
    if count > threshold and (current_time - last_alert_time > cooldown):
        alert_message = f"The area is exceeding the limit of {threshold} people."

        # Voice alert
        try:
            engine.say(alert_message)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ TTS failed: {e}")

        # SMS alert
        try:
            message = twilio_client.messages.create(
                body=alert_message,
                from_=twilio_phone_number,
                to=destination_phone_number
            )
            print(f"📩 SMS sent: {message.sid}")
        except Exception as e:
            print(f"⚠️ Failed to send SMS: {e}")

        last_alert_time = current_time

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Quitting...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
