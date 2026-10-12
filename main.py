import cv2
import time
import platform

# Windows provides winsound. On other operating systems, the program still runs
# but prints an alert instead of playing a beep.
try:
    import winsound
except ImportError:
    winsound = None

CAMERA_INDEX = 0
CLOSED_EYE_FRAME_LIMIT = 20   # Increase this to reduce false alarms
ALARM_INTERVAL_SECONDS = 2.0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

if face_cascade.empty() or eye_cascade.empty():
    raise RuntimeError("OpenCV Haar cascade files could not be loaded.")

camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened():
    raise RuntimeError(
        "Could not open the webcam. Check that a camera is connected "
        "and close other applications using it."
    )

closed_eye_frames = 0
last_alarm_time = 0.0

print("Drowsiness Detection System started.")
print("Keep your face visible to the webcam. Press Q to quit.")

try:
    while True:
        success, frame = camera.read()
        if not success:
            print("Could not read a frame from the webcam.")
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(80, 80)
        )

        status = "Monitoring"
        color = (0, 200, 0)

        if len(faces) > 0:
            # Use the largest detected face.
            x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
            face_gray = gray[y:y + h, x:x + w]
            face_color = frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(
                face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15)
            )

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 180, 0), 2)

            for ex, ey, ew, eh in eyes:
                cv2.rectangle(
                    face_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                )

            # This simple beginner project treats repeated failure to detect
            # eyes as a possible drowsiness signal. It is not a medical device.
            if len(eyes) < 2:
                closed_eye_frames += 1
            else:
                closed_eye_frames = 0

            if closed_eye_frames >= CLOSED_EYE_FRAME_LIMIT:
                status = "WARNING: POSSIBLE DROWSINESS!"
                color = (0, 0, 255)
                now = time.time()
                if now - last_alarm_time >= ALARM_INTERVAL_SECONDS:
                    if winsound is not None:
                        try:
                            winsound.Beep(2000, 500)
                        except RuntimeError:
                            print("ALERT: Possible drowsiness detected!")
                    else:
                        print("ALERT: Possible drowsiness detected!")
                    last_alarm_time = now
        else:
            status = "Face not detected"
            color = (0, 165, 255)
            closed_eye_frames = 0

        cv2.putText(
            frame, status, (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, color, 2, cv2.LINE_AA
        )
        cv2.putText(
            frame, "Press Q to quit", (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA
        )

        cv2.imshow("Drowsiness Detection System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
    print("Drowsiness Detection System stopped.")
