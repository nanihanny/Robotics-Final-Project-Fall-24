import requests

esp32_ip = "http://172.20.1.58"  
servo_endpoint = f"{esp32_ip}/servo"

def set_servo_angle(angle):
    if 0 <= angle <= 180:
        params = {'angle': angle}
        try:
            response = requests.get(servo_endpoint, params=params)
            if response.status_code == 200:
                print(f"Success: {response.text}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Angle must be between 0 and 180.")

# set_servo_angle(120)  
# set_servo_angle(120) 