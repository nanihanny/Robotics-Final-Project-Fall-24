import requests

# ESP32 IP address
esp32_ip = "http://172.20.1.58"  # Replace with the actual IP address of your ESP32
servo_endpoint = f"{esp32_ip}/servo"

# Function to set the servo angle
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

# Example usage
#set_servo_angle(120)  # Move the servo to 90 degrees