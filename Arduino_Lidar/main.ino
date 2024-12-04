#include "RPLidar.h"
#include "movement.h"
#include "data_transfer.h"
#include <WiFiClient.h>

#define RPLIDAR_MOTOR 8 // Pin to control motor (can change on set)
#define NUM_CAMERA_SCAN 10 // Number of rotations for camera to view
#define NUM_DEGREES 10 // Number of degrees required before sending data to computer
#define SPEED 150
int orientation = 0;
int rotate_to_cup = 5;
int move_to_cup = 5;

const char ssid[] = "Knightshade_Resident";         // Wi-Fi Network Name
const char pass[] = "rose007kind";     // Wi-Fi Password

// create driver instance
RPLidar lidar;                 

                   
void setup() {
  setup_Motors();
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(10000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");
 // send_data1("Connected");

  // // Set up LiDAR motor control
  // pinMode(RPLIDAR_MOTOR, OUTPUT);
  // analogWrite(RPLIDAR_MOTOR, 255); // Start LiDAR motor

  // Bind LiDAR driver to Arduino hardware serial
  Serial1.begin(115200);
  // lidar.begin(Serial1);

  // Start LiDAR scanning
  // if (IS_OK(lidar.startScan())) {
  //   Serial.println("LiDAR started successfully.");
  // } else {
  //   Serial.println("Failed to start LiDAR.");
  // }
}
bool found = false;
bool move_back = false;
int total_dist = 0;
int total_angle = 0;
void loop() {
  // collect data from lidar
  // String data_lidar = scan_lidar(lidar);
  
  // collect data fron camera
  Serial.println("Bool is: " + String(found));

  if(!found){
    found = scan_camera();
    move_back = true;
  }else if(move_back){
    delay(2000);
    move_back = false;
    turnAngle(-total_angle*1.8 , SPEED/6);
    moveDistance(total_dist*1.25, SPEED/3);

  }
  
  // // If the cup is not found, continue to search with lidar data
  // if(!found){
  //   send_data1(data_lidar);
  // }

  // // Receive instructions to move robot to next position
  // data_lidar = get_data1();

  // // The data string holds the path for the robot to follow
  // String data[50];
  // int len = 0, b = 0;

  // // Decipher data sent from computer
  // for(int i=0; i<data_lidar.length(); i++){
  //   if(data_lidar.charAt(i) == ','){
  //     data[len] = data_lidar.substring(b, i);
  //     b = i+1;
  //     len++;
  //   }
  // }
  // len--;

  // // orientate the robot in the correct direction
  // if(orientation != data[0].toInt())
  //   turnAngle(data[0].toInt() - orientation, SPEED);

  // // follow path instructions
  // for(int i = 1; i < len - 1; i+2){
  //   moveDistance(data[i].toInt(), SPEED);
  //   delay(1000);
  //   turnAngle(data[i+1].toInt(), SPEED);
  //   orientation += data[i+1].toInt();
  // }
}

bool scan_camera(){
  int angle, distance;
  bool flag = false;

  // Check if camera's view has the red object 
  for(int i = 0; i < NUM_CAMERA_SCAN; i++){
    // get data from camera
    String data_camera = get_data2();
    Serial.println("Turn Number: " + String(i));
    String new_data_camera = parseCommand(data_camera);
    

    // follow camera's instructions to center robot with red object
    while(!new_data_camera.equals("N")){
      Serial.println("in the loop");
      Serial.println(String(new_data_camera ));

      if(new_data_camera.equals("L")){

        Serial.println(String(new_data_camera ));
        turnAngle(-rotate_to_cup, SPEED);
        orientation -= rotate_to_cup;
        total_angle -= rotate_to_cup;
      }else if(new_data_camera.equals("R")){
        Serial.println(String(new_data_camera ));
        turnAngle(rotate_to_cup, SPEED);
        orientation += rotate_to_cup;
        total_angle += rotate_to_cup;
      }else if(new_data_camera.equals("F")){
        Serial.println(String(new_data_camera ));
        moveDistance(move_to_cup, 125);
        total_dist += move_to_cup;
      }else if(new_data_camera.equals("S")){
          Serial.println(String(new_data_camera ));

        return true;
      }//else{
        // Find distance to red object for path planning
      //   while((angle = int(lidar.getCurrentPoint().angle)) != 0)
      //     lidar.waitPoint();

      //   distance = int(lidar.getCurrentPoint().distance / 10);

      //   String data = "Target," + String(orientation) + ","  + String(distance);
      //  // send_data1(data);

      //   flag = true;
      //   break;
      //}

      data_camera =  get_data2();
      new_data_camera = parseCommand(data_camera);
    }
    if(!flag){
      turnAngle(45, SPEED/2);
      orientation += 90;
      total_angle += 45;
      delay(1000);
    }
  }
  return flag;
}

String parseCommand(String response) {
  // Extract the command value from the JSON response
  int start = response.indexOf(":") + 2;  // Find the starting index of the command
  int end = response.lastIndexOf("\"");  // Find the closing quote
  if (start > 0 && end > start) {
    return response.substring(start, end);  // Extract and return the command
  }
  return "";  // Return an empty string if parsing fails
}

String scan_lidar(RPLidar lidar) {
  int degrees_received = 0;
  int degree[360];

  // Initialize degree array
  for (int i = 0; i < 360; i++) {
    degree[i] = -1;
  }

  int angle, distance;
  while (degrees_received < NUM_DEGREES) {
    if (IS_OK(lidar.waitPoint())) {
      // Collect angle and distance
      angle = int(lidar.getCurrentPoint().angle) % 360;  // Ensure angle is 0-359
      distance = int(lidar.getCurrentPoint().distance / 10);

      // Check if angle has already been received
      if (degree[angle] == -1) {
        degree[angle] = distance;
        degrees_received++;
        //send_data1("Adding Data: " + String(degrees_received) + " " + String(distance));
      }
    } else {
      // Handle LiDAR error recovery
      analogWrite(RPLIDAR_MOTOR, 0); // Stop motor
      lidar.stop();                 // Stop scanning
      delay(100);

      if (IS_OK(lidar.startScan())) {
        analogWrite(RPLIDAR_MOTOR, 255); // Restart motor
        Serial.println("LiDAR restarted successfully.");
      } else {
        Serial.println("LiDAR restart failed.");
      }
    }
  }

  // Create data string of LiDAR info
  String data = "Scan,";
  for (int i = 0; i < 360; i++) {
    if (degree[i] == -1) {
      data += String(-1) + ",";
    } else {
      data += String(degree[i]) + ",";
    }
  }

  //send_data1(data);  // Send data to computer
  return data;
}