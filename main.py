import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import subprocess

cap = cv2.VideoCapture(0)

base_options = python.BaseOptions(
    model_asset_path="C:/Users/USER/Documents/Python/Project_PRISM/models/hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)

gesture_state = "IDLE"
swipe_start_x = None

SWIPE_DISTANCE = 0.15

def execute_gesture(direction):

    if direction == "right":
        print("PRISM SYSTEMS: Right Movement Detected.")
        print("PRISM SYSTEMS: Executing RIGHT command.")
        print("PRISM SYSTEMS: Initializing workspace...")
        print("Starting up ChatGPT, Youtube and Claude")

        subprocess.Popen(
                ["cmd", "/c", "start", "", "chrome", 
                "https://claude.ai/new"]
            )

        subprocess.Popen(
                ["cmd", "/c", "start", "", "chrome", 
                "https://www.chatgpt.com"]
            )

        subprocess.Popen(
                ["cmd", "/c", "start", "", "chrome", 
                 "https://www.youtube.com"]
            )       

        print("PRISM SYSTEMS: Workspace Initialized Successfully.")


    elif direction == "left":
        print("PRISM SYSTEMS: Left Movement Detected.")
        print("PRISM SYSTEMS: Executing LEFT command.")
        print("PRISM SYSTEMS: Minimizing workspace...")

        subprocess.run(
            [
                "powershell", 
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject Shell.Application).MinimizeAll()"
            ]
        )

        print("PRISM SYSTEMS: Workspace Minimized successfully.")

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

print("---------------------------------------------------------------------------------------------------------------")
print("Hello Master, Starting PRISM Systems...")
print("PRISM Systems initializing...")
print("---------------------------------------------------------------------------------------------------------------")

while True:
    success, frame = cap.read()

    if not success:
        print("Could not access camera. Prism Systems could not be initialized.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = frame_rgb
    )

    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:

        for hand in detection_result.hand_landmarks:

            points = []

            wrist = detection_result.hand_landmarks[0][0]

            current_x = wrist.x

            if gesture_state == "IDLE":

                swipe_start_x = current_x
                gesture_state = "TRACKING"

            elif gesture_state == "TRACKING":

                distance = current_x -swipe_start_x

                if distance > SWIPE_DISTANCE:

                    execute_gesture("left")

                    gesture_state = "COOLDOWN"
                    swipe_start_x = None

                elif distance < -SWIPE_DISTANCE:

                    execute_gesture("right")

                    gesture_state = "COOLDOWN"
                    swipe_start_x = None

            elif gesture_state == "COOLDOWN":

                swipe_start_x = None
                gesture_state = "IDLE"

            for landmark in hand:

                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                points.append((x, y))

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            for start, end in HAND_CONNECTIONS:

                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    (255, 0, 0),
                    2
                )

    cv2.imshow("PRISM SYSTEMS, Status: ONLINE", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("---------------------------------------------------------------------------------------------------------------")
print("PRISM Systems have been terminated successfully.")
print("Goodbye Master, have a great day !.")
print("---------------------------------------------------------------------------------------------------------------")
