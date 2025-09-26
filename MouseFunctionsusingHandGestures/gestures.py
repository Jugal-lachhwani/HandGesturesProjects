from utils import *

def is_left_click(landmarks_list):
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) > 50 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) < 45 and 
        get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12]) > 90
        )

def is_right_click(landmarks_list):
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) > 50 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) > 90 and 
        get_angle(landmarks_list[9],landmarks_list[11],landmarks_list[12]) < 45
        )

def is_double_click(landmarks_list):
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) > 50 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) < 45 and 
        get_angle(landmarks_list[9],landmarks_list[11],landmarks_list[12]) < 45
        )

def is_screenshot(landmarks_list):
    return ( 
            get_distance([landmarks_list[4],landmarks_list[5]]) < 50 and 
        get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) < 45 and 
        get_angle(landmarks_list[9],landmarks_list[11],landmarks_list[12]) < 45
        )
        
