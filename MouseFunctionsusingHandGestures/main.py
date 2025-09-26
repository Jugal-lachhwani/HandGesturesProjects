import cv2
import random
import mediapipe as mp
from utils import *
import pyautogui
from pynput.mouse import Button, Controller
from gestures import *

mouse = Controller()
screen_width,screen_height = pyautogui.size()

mphands = mp.solutions.hands
hands = mphands.Hands(
    static_image_mode = False,
    model_complexity = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7,
    max_num_hands = 1
)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]
    
    return None

def move_mouse(index_finger_tip):
     if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x,y)
        
def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = get_distance([landmarks_list[4],landmarks_list[5]])
        index_finger_angle = get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])
        
        
        if thumb_index_dist < 50 and index_finger_angle > 90:
            move_mouse(index_finger_tip)
        
        elif is_left_click(landmarks_list):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmarks_list):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmarks_list):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmarks_list):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
def main():  
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret,frame = cap.read()
            landmarks_list = []
            
            if ret == False:
                break
            frame = cv2.flip(frame,1)
            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            processed = hands.process(frameRGB)
            
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame,hand_landmarks,mphands.HAND_CONNECTIONS)
                
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x,lm.y))
                    
            detect_gestures(frame, landmarks_list, processed)
            
            cv2.imshow('Frame',frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()