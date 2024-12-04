import cv2
import urllib.request
import numpy as np

import requests
import http_servo as servo

flask_url = 'http://127.0.0.1:5000/process' 

camera_url = 'http://172.20.5.50/cam-hi.jpg'


def send_command_to_server(command): 
    data = {'data': command}
    try:
        response = requests.post(flask_url, data=data)
        if response.status_code == 200:
            print(f"Command {command} sent successfully!")
        else:
            print(f"Failed to send command {command}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")

def detect_red_cups(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    red_area = cv2.bitwise_and(image, image, mask=mask)
    
    gray = cv2.cvtColor(red_area, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = contours[0]
        
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        min_width = 50
        min_height = 50
        
        if w >= min_width and h >= min_height:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            return x + w // 2, h, w, image
    
    return None, None, None, image
def run2():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    global response
    while True:
        img_resp = urllib.request.urlopen(camera_url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        
        object_center_x, object_height, object_width, im_with_detection = detect_red_cups(im)
        
        frame_center_x = im.shape[1] // 2
        
        if object_center_x is not None:
            if abs(object_center_x - frame_center_x) <= 95:
                if object_height > im.shape[0] * 0.80 and object_width > im.shape[1] * 0.65: 
                    send_command_to_server('S')  # Stop
                    print("S")
                    cv2.waitKey(100)
                    servo.set_servo_angle(0)
                    return
                else:
                    send_command_to_server('F') 
                    print("F")
            else:
                if object_center_x < frame_center_x:
                    send_command_to_server('R')  
                    print("R")
                else:
                   send_command_to_server('L')
                   print("L")
        else:
            send_command_to_server('N')
            print("N")

        flipped_image = cv2.flip(im_with_detection, 0)

        cv2.imshow('detection', flipped_image)

        key = cv2.waitKey(15)
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()


if __name__ == '__main__':
    servo.set_servo_angle(120)
    servo.set_servo_angle(120)
    run2()
