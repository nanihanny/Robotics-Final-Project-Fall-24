#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>


// WiFi credentials
const char* ssid = "Knightshade_Resident";
const char* password = "rose007kind";

// Create a web server object on port 80
AsyncWebServer server(80);

// Servo object
Servo myServo;
int servoPin = 27; // GPIO pin for the servo
int currentAngle = 120; // Initial servo angle

void setup() {
  // Start Serial Monitor
  Serial.begin(115200);

  // Attach the servo
  myServo.attach(servoPin);
  myServo.write(currentAngle); // Set to initial position

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Define HTTP routes
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "Send an HTTP GET to /servo?angle=<0-180>");
  });

  server.on("/servo", HTTP_GET, [](AsyncWebServerRequest *request) {
    if (request->hasParam("angle")) {
      String angleParam = request->getParam("angle")->value();
      int angle = angleParam.toInt();
      if (angle >= 0 && angle <= 180) {
        Serial.print("angle" + String(angle));
        
        //myServo.write(angle)
        
        for(int i=currentAngle; i>=angle ; i--){
          myServo.write(i);
          delay(10);
        }

        currentAngle= angle;
        request->send(200, "text/plain", "Servo angle set to " + String(angle));
      } else {
        request->send(400, "text/plain", "Invalid angle. Use values between 0 and 180.");
      }
    } else {
      request->send(400, "text/plain", "Missing 'angle' parameter.");
    }
  });

  // Start server
  server.begin();
}

void loop() {
  // Nothing needed here for AsyncWebServer
}
