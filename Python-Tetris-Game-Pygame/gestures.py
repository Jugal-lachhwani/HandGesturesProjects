from utils import *
import mediapipe as mp

frame_width = 500
frame_height = 620  # Fixed typo
screen_width = 500  # Added missing variable
screen_height = 620  # Added missing variable
mp_hands = mp.solutions.hands

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    return None

from_pos = None
def move_block_left(index_finger_tip,landmarks_list):
    global from_pos
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        if not from_pos:
            from_pos = x
        print("from_pos =", from_pos, "x =", x)
        if get_distance([landmarks_list[4],landmarks_list[5]]) > 100 and (from_pos - x) > 30:
            from_pos = x
            return True
        return False
    return False

def move_block_right(index_finger_tip,landmarks_list):
    global from_pos
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        if not from_pos:
            from_pos = x
        if get_distance([landmarks_list[4],landmarks_list[5]]) > 100 and (x - from_pos) > 30:
            from_pos = x
            return True
        return False
    return False

def is_rotate(landmarks_list):
    print(get_distance([landmarks_list[4],landmarks_list[5]]))
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) < 75 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) < 45 and 
        get_angle(landmarks_list[9],landmarks_list[11],landmarks_list[12]) < 45
        )
def is_rotate(landmarks_list):
    print(get_distance([landmarks_list[4],landmarks_list[5]]))
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) > 75 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) < 45 and 
        get_angle(landmarks_list[9],landmarks_list[11],landmarks_list[12]) < 45
        )
def is_index_finger_down(landmarks_list):
    """Check if index finger is pointing down (fast drop gesture)"""
    if len(landmarks_list) < 21:
        return False
def is_index_finger_down(landmarks_list):
    """Check if index finger is pointing down (fast drop gesture)"""
    if len(landmarks_list) < 21:
        return False
    
    # Check if only index finger is extended (others closed)
    # Index finger extended: tip (8) is above PIP (6)
    index_extended = landmarks_list[8][1] < landmarks_list[6][1]
    
    wrist_y = landmarks_list[0][1]
    index_tip_y = landmarks_list[8][1]
    
    # Check if index finger tip is below the wrist
    # In image coordinates, y increases downward, so lower means higher y value
    index_below_wrist = index_tip_y > wrist_y
    # Other fingers closed: tips below PIP joints
    middle_closed = landmarks_list[12][1] > landmarks_list[10][1]
    ring_closed = landmarks_list[16][1] > landmarks_list[14][1]
    pinky_closed = landmarks_list[20][1] > landmarks_list[18][1]
    
    # Thumb should be close to palm (optional check)
    thumb_closed = get_distance([landmarks_list[4], landmarks_list[5]]) < 50
    
    return index_below_wrist and middle_closed and pinky_closed and ring_closed