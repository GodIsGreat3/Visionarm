import time
import cv2
import numpy as np
import serial
import serial.tools.list_ports
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont

PORT = None
BAUD = 9600
STABLE_FRAMES = 6

GESTURES = {
    1: ("3", "Схватить"),
    2: ("4", "Отпустить"),
    3: ("1", "Опустить"),
    4: ("2", "Поднять"),
    5: ("2", "Поднять"),
}

def find_port():
    for p in serial.tools.list_ports.comports():
        d = (p.description or "").lower()
        if "arduino" in d or "ch340" in d or "usb serial" in d or "acm" in p.device.lower():
            return p.device
    return None

port = PORT or find_port()
if port is None:
    raise SystemExit("Arduino не найдена. Укажите PORT вручную.")
arduino = serial.Serial(port, BAUD, timeout=0.1)
time.sleep(2)
print("Подключено к", port)

FONT_PATHS = [
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
font = None
for p in FONT_PATHS:
    try:
        font = ImageFont.truetype(p, 36)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

def put_text(frame, text, pos=(20, 20), color=(0, 255, 0)):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ImageDraw.Draw(img).text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def dist(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

def count_fingers(lm):
    wrist = lm[0]
    count = 0
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if dist(lm[tip], wrist) > dist(lm[pip], wrist) * 1.1:
            count += 1
    if dist(lm[4], lm[17]) > dist(lm[3], lm[17]) * 1.05 and \
       dist(lm[4], lm[5]) > 0.1 * dist(lm[0], lm[9]) * 3:
        count += 1
    return count

cap = cv2.VideoCapture(0)
last_seen = None
stable = 0
last_sent = None
status = ""

with mp_hands.Hands(max_num_hands=1,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.6) as hands:
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        n = 0
        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            n = count_fingers(hand.landmark)

        if n == last_seen and n in GESTURES:
            stable += 1
        else:
            stable = 0
            last_seen = n

        if stable == STABLE_FRAMES:
            cmd, label = GESTURES[n]
            if cmd != last_sent:
                arduino.write(cmd.encode())
                last_sent = cmd
                status = f"{label} (пальцев: {n})"
                print("Отправлено:", cmd, label)

        if n == 0:
            last_sent = None

        frame = put_text(frame, f"Пальцев: {n}", (20, 20))
        if status:
            frame = put_text(frame, status, (20, 70), (0, 200, 255))

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
arduino.close()
