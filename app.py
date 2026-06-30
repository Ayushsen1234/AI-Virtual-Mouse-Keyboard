import cv2
import pyautogui
import math
import numpy as np
from hand_detector import HandDetector
from virtual_keyboard import create_buttons, draw_keyboard

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

dragging = False
double_clicked = False
left_clicked = False
right_clicked = False

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector()

screen_w, screen_h = pyautogui.size()

smoothening = 7
prev_x, prev_y = 0, 0

button_list = create_buttons()

while True:

    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    frame, landmarks = detector.find_hands(frame)

    h, w, _ = frame.shape

    # ✅ Canvas (camera + keyboard area)
    keyboard_height = 420
    canvas = cv2.copyMakeBorder(
        frame,
        0,
        keyboard_height,
        0,
        0,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0)
    )

    if landmarks:

        # Fingers
        x, y = landmarks[8][1], landmarks[8][2]
        thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]
        middle_x, middle_y = landmarks[12][1], landmarks[12][2]
        ring_x, ring_y = landmarks[16][1], landmarks[16][2]

        # Mouse move
        screen_x = int((x / w) * screen_w)
        screen_y = int((y / h) * screen_h)

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening

        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # Distances
        left_distance = math.hypot(x - thumb_x, y - thumb_y)
        right_distance = math.hypot(middle_x - thumb_x, middle_y - thumb_y)
        double_distance = math.hypot(ring_x - thumb_x, ring_y - thumb_y)
        drag_distance = math.hypot(x - middle_x, y - middle_y)

        # Left click
        if left_distance < 40 and not left_clicked:
            pyautogui.click()
            left_clicked = True
        elif left_distance >= 40:
            left_clicked = False

        # Right click
        if right_distance < 40 and not right_clicked:
            pyautogui.rightClick()
            right_clicked = True
        elif right_distance >= 40:
            right_clicked = False

        # Double click
        if double_distance < 40 and not double_clicked:
            pyautogui.doubleClick()
            double_clicked = True
        elif double_distance >= 40:
            double_clicked = False

        # Drag
        if drag_distance < 45 and not dragging:
            pyautogui.mouseDown()
            dragging = True
        elif drag_distance >= 45 and dragging:
            pyautogui.mouseUp()
            dragging = False

        # =========================
        # KEYBOARD LOGIC (FIXED)
        # =========================

        ix, iy = landmarks[8][1], landmarks[8][2]

        for button in button_list:
            bx, by = button.pos
            bw, bh = button.size

            if bx < ix < bx + bw and by < iy < by + bh:

                cv2.rectangle(canvas, (bx, by), (bx + bw, by + bh), (0, 255, 0), cv2.FILLED)
                cv2.putText(canvas, button.text,
                            (bx + 20, by + 45),
                            cv2.FONT_HERSHEY_PLAIN,
                            2,
                            (255, 255, 255),
                            2)

                distance = math.hypot(ix - thumb_x, iy - thumb_y)

                if distance < 40:
                    if button.text == "SPACE":
                        pyautogui.write(" ")
                    elif button.text == "BACKSPACE":
                        pyautogui.press("backspace")
                    elif button.text == "ENTER":
                        pyautogui.press("enter")
                    else:
                        pyautogui.write(button.text)

                    cv2.rectangle(canvas, (bx, by), (bx + bw, by + bh), (255, 0, 0), 3)

        # Draw points
        cv2.circle(canvas, (x, y), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(canvas, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(canvas, (middle_x, middle_y), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(canvas, (ring_x, ring_y), 10, (255, 0, 255), cv2.FILLED)

        cv2.putText(canvas, f"Left: {int(left_distance)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(canvas, f"Right: {int(right_distance)}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.putText(canvas, f"Double: {int(double_distance)}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        cv2.putText(canvas, f"Drag: {int(drag_distance)}", (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    # Draw keyboard
    canvas = draw_keyboard(canvas, button_list)

    cv2.imshow("AI Virtual Mouse Pro", canvas)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()