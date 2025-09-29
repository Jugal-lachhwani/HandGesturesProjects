import pygame,sys
from game import Game
from colors import Colors
import cv2
import mediapipe as mp
from utils import *

# --- Setup Mediapipe Hands ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

cap = cv2.VideoCapture(0)
draw = mp.solutions.drawing_utils

frame_width = 500
frame_height = 620  # Fixed typo
screen_width = 500  # Added missing variable
screen_height = 620  # Added missing variable

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()
game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)  # This handles automatic block movement

from_pos = None
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    return None

def move_block_left(index_finger_tip, thumb_index_dist, index_finger_angle):
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

def move_block_right(index_finger_tip, thumb_index_dist, index_finger_angle):
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

while True:
    # Process camera feed OUTSIDE the event loop
    ret, frame = cap.read()
    landmarks_list = []
    index_finger_tip = None
    thumb_index_dist = 0
    index_finger_angle = 0
    
    if ret:
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed = hands.process(frameRGB)
        
        if processed.multi_hand_landmarks:
            hand_landmarks = processed.multi_hand_landmarks[0]
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # Fixed typo
            
            for lm in hand_landmarks.landmark:
                landmarks_list.append((lm.x, lm.y))
            
            # Calculate gesture parameters
            if len(landmarks_list) >= 21:
                index_finger_tip = find_finger_tip(processed)
                thumb_index_dist = get_distance([landmarks_list[4], landmarks_list[5]])
                index_finger_angle = get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])
        
        small_frame = cv2.resize(frame, (200, 150))  # Small size
        cv2.imshow('Hand Tracking', small_frame)
        cv2.moveWindow('Hand Tracking', 680, 470)
        
    
    # Process pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        
        # AUTOMATIC BLOCK MOVEMENT (This is what you want to keep!)
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()  # Blocks fall automatically every 200ms
        
        # Keyboard controls (backup)
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
    
    # Handle gesture controls OUTSIDE the event loop
    if len(landmarks_list) >= 21 and game.game_over == False:
        # Gesture controls for left/right movement only
        if move_block_left(index_finger_tip, thumb_index_dist, index_finger_angle):
            game.move_left()
        if move_block_right(index_finger_tip, thumb_index_dist, index_finger_angle):
            game.move_right()
        if is_rotate(landmarks_list):
            game.rotate()
            
        
        # Add gesture for rotation if needed
        # You can add rotation gesture here
    
    # Reset game on game over
    if game.game_over == True:
        # You can add a gesture to reset the game here
        pass
    
    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50, 50))
    
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, 
        centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)
    
    pygame.display.update()
    clock.tick(60)
    
    # Allow OpenCV to process events
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()