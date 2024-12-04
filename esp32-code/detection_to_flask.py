import cv2
import urllib.request
import numpy as np
import concurrent.futures

#import data_collection

import requests
import http_servo as servo


flask_url = 'http://127.0.0.1:5000/process' #flask command
#response = 'o'
#url = 'http://localhost:5000/process'
#data = {'data': 'AAAHHHH'}

# Camera feed URL for both cams RETREAT WEST
camera_url = 'http://172.20.5.50/cam-hi.jpg'

#url = 'http://172.20.6.140/cam-hi.jpg'

# Camera feed URL for both cams KRISS HOUSE
#url = 'http://192.168.1.87/cam-lo.jpg'

#url = 'http://192.168.1.88/cam-lo.jpg'

def send_command_to_server(command): 
    return 
    data = {'data': command}
    try:
        response = requests.post(flask_url, data=data)
        if response.status_code == 200:
            print(f"Command {command} sent successfully!")
        else:
            print(f"Failed to send command {command}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")

# Helper function to detect red cups and find their position
def detect_red_cups(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range for red color in HSV
    lower_red1 = np.array([0, 60, 40])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 60, 40])
    upper_red2 = np.array([180, 255, 255])
    
    # Create a mask for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Bitwise-AND the mask and the original image to extract red areas
    red_area = cv2.bitwise_and(image, image, mask=mask)
    
    # Convert to grayscale to detect contours
    gray = cv2.cvtColor(red_area, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Find contours in the image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Sort contours by area, descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = contours[0]
        
        # Get bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Define a minimum size threshold
        min_width = 30
        min_height = 30
        
        # Check if the bounding box meets the minimum size requirement
        if w >= min_width and h >= min_height:
            # Draw a rectangle around the detected red cup
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Return the x-coordinate of the center and height of the bounding box
            return x + w // 2, h, w, image
    
    return None, None, None, image
def run2():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    global response
    while True:
        # Fetch image from the URL
        img_resp = urllib.request.urlopen(camera_url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        
        # Detect red cups and get their horizontal position and size
        object_center_x, object_height, object_width, im_with_detection = detect_red_cups(im)
        
        # Determine the frame's center
        frame_center_x = im.shape[1] // 2
        
        if object_center_x is not None:
            # Check if the object is centered
            if abs(object_center_x - frame_center_x) <= 50:
                # If centered, check the proximity (height of the object)
                if object_height > im.shape[0] * 0.90 and object_width > im.shape[1] * 0.60:  # Example: object fills 50% of frame height
                    send_command_to_server('S')  # Stop
                    print("S")
                    cv2.waitKey(100)
                    servo.set_servo_angle(35)
                else:
                    send_command_to_server('F') 
                    print("F")
            else:
                # Provide recentering instructions
                if object_center_x < frame_center_x:
                    send_command_to_server('L')  # Move Left
                    print("L")
                else:
                   send_command_to_server('R')  # Move Left
                   print("R")
        else:
            send_command_to_server('N')  # Move Left
            print("N")

        
        # Show the image with detection
        cv2.imshow('detection', im_with_detection)
        
        # Quit on pressing 'q'
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    servo.set_servo_angle(120)
    servo.set_servo_angle(120)
    run2()
   # print("Started detection")
   # response = requests.post(url, data=data)
  #  with concurrent.futures.ProcessPoolExecutor() as executor:
       # executor.submit(run2)
