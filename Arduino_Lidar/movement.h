#include <Encoder.h>

#define MOTOR_L_DIR1 4
#define MOTOR_L_DIR2 5

#define MOTOR_R_DIR1 2
#define MOTOR_R_DIR2 3

#define ENCODER_L_A 6
#define ENCODER_L_B 7
#define ENCODER_R_A 0
#define ENCODER_R_B 1

#define WHEEL_DIAMETER 7.62
#define TICKS_PER_REV 408
#define WHEEL_BASE 10

#define TURN_RATIO 0.08333
#define DISTANCE_RATIO 4.35

Encoder leftEncoder(ENCODER_L_A, ENCODER_L_B);
Encoder rightEncoder(ENCODER_R_A, ENCODER_R_B);

volatile long leftEncoderTicks = 0;
volatile long rightEncoderTicks = 0;
float robotX = 0, robotY = 0, robotTheta = 0;

// set correct pins to motors
void setup_Motors(){
  pinMode(MOTOR_L_DIR1, OUTPUT);
  pinMode(MOTOR_L_DIR2, OUTPUT);
  
  pinMode(MOTOR_R_DIR1, OUTPUT);
  pinMode(MOTOR_R_DIR2, OUTPUT);

  leftEncoder.write(0);
  rightEncoder.write(0);

  Serial.begin(115200);
}

// move motors in correct direction for use
void setMotorSpeed(int motor, int speed){
  if (motor == 0){
    if (speed > 0){
      digitalWrite(MOTOR_L_DIR1, HIGH);
      digitalWrite(MOTOR_L_DIR2, LOW);
    }else{
      digitalWrite(MOTOR_L_DIR1, LOW);
      digitalWrite(MOTOR_L_DIR2, HIGH);
    }
  }else if (motor == 1){
    if (speed > 0){
      digitalWrite(MOTOR_R_DIR1, HIGH);
      digitalWrite(MOTOR_R_DIR2, LOW);
    }else{
      digitalWrite(MOTOR_R_DIR1, LOW);
      digitalWrite(MOTOR_R_DIR2, HIGH);
    } 
  }
}

// stops motores
void stopMotors(){
  digitalWrite(MOTOR_L_DIR1, LOW);
  digitalWrite(MOTOR_L_DIR2, LOW);
  digitalWrite(MOTOR_R_DIR1, LOW);
  digitalWrite(MOTOR_R_DIR2, LOW);
}

void updateOdometry(){
  long leftTicks = leftEncoder.read();
  long rightTicks = rightEncoder.read();

  float leftDistance = (leftTicks / (float)TICKS_PER_REV) * PI * WHEEL_DIAMETER;
  float rightDistance = (rightTicks / (float)TICKS_PER_REV) * PI * WHEEL_DIAMETER;
  float distance = (leftDistance + rightDistance) / 2.0;

  float deltaTheta = (rightDistance - leftDistance) / WHEEL_BASE;
  robotTheta += deltaTheta;
  robotX += distance * cos(robotTheta);
  robotY += distance * sin(robotTheta);

  leftEncoder.write(0);
  rightEncoder.write(0);
}

// move robot forward targetDistance forward
void moveDistance(float targetDistance, int speed){
  targetDistance = targetDistance * DISTANCE_RATIO;
  long targetTicks = (targetDistance / (PI * WHEEL_DIAMETER)) * TICKS_PER_REV;
  leftEncoder.write(0);
  rightEncoder.write(0);

  while (abs(leftEncoder.read()) < targetTicks && abs(rightEncoder.read()) < targetTicks){
    setMotorSpeed(0, speed);
    setMotorSpeed(1, speed);
  }
  stopMotors();
}

// turn the robot x amount of degrees (positive->right or negative->left)
void turnAngle(float angle, int speed){
  angle = angle * TURN_RATIO;
  float tmp_angle = abs(angle);
  float targetArcLength = (WHEEL_BASE * tmp_angle) / 2.0;
  long targetTicks = (targetArcLength / (PI * WHEEL_DIAMETER)) * TICKS_PER_REV;

  leftEncoder.write(0);
  rightEncoder.write(0);

  if (angle > 0){
    while (abs(rightEncoder.read()) < targetTicks){
      setMotorSpeed(0, speed);
      setMotorSpeed(1, -speed);
    }
  }else{
    while (abs(rightEncoder.read()) < targetTicks){
      setMotorSpeed(0, -speed);
      setMotorSpeed(1, speed);
    }
  }
  stopMotors();
}
