#include <Encoder.h>

#define MOTOR_L_PWM 5
#define MOTOR_L_DIR1 4
#define MOTOR_L_DIR2 7
#define MOTOR_R_PWM 6
#define MOTOR_R_DIR1 8
#define MOTOR_R_DIR2 9

#define ENCODER_L_A 2
#define ENCODER_L_B 22
#define ENCODER_R_A 3
#define ENCODER_R_B 23

#define WHEEL_DIAMETER 0.065
#define TICKS_PER_REV 360
#define WHEEL_BASE 0.15
#define SPEED 150

Encoder leftEncoder(ENCODER_L_A, ENCODER_L_B);
Encoder rightEncoder(ENCODER_R_A, ENCODER_R_B);

volatile long leftEncoderTicks = 0;
volatile long rightEncoderTicks = 0;
float robotX = 0, robotY = 0, robotTheta = 0;

void setMotorSpeed(int motor, int speed)
{
    if (motor == 0)
    {
        if (speed > 0)
        {
            digitalWrite(MOTOR_L_DIR1, HIGH);
            digitalWrite(MOTOR_L_DIR2, LOW);
        }
        else
        {
            digitalWrite(MOTOR_L_DIR1, LOW);
            digitalWrite(MOTOR_L_DIR2, HIGH);
        }
        analogWrite(MOTOR_L_PWM, abs(speed));
    }
    else if (motor == 1)
    {
        if (speed > 0)
        {
            digitalWrite(MOTOR_R_DIR1, HIGH);
            digitalWrite(MOTOR_R_DIR2, LOW);
        }
        else
        {
            digitalWrite(MOTOR_R_DIR1, LOW);
            digitalWrite(MOTOR_R_DIR2, HIGH);
        }
        analogWrite(MOTOR_R_PWM, abs(speed));
    }
}

void stopMotors()
{
    analogWrite(MOTOR_L_PWM, 0);
    analogWrite(MOTOR_R_PWM, 0);
    digitalWrite(MOTOR_L_DIR1, LOW);
    digitalWrite(MOTOR_L_DIR2, LOW);
    digitalWrite(MOTOR_R_DIR1, LOW);
    digitalWrite(MOTOR_R_DIR2, LOW);
}

void updateOdometry()
{
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

void moveDistance(float targetDistance, int speed)
{
    long targetTicks = (targetDistance / (PI * WHEEL_DIAMETER)) * TICKS_PER_REV;
    leftEncoder.write(0);
    rightEncoder.write(0);

    while (abs(leftEncoder.read()) < targetTicks && abs(rightEncoder.read()) < targetTicks)
    {
        setMotorSpeed(0, speed);
        setMotorSpeed(1, speed);
        updateOdometry();
    }
    stopMotors();
}

void turnAngle(float angle, int speed)
{
    float targetArcLength = (WHEEL_BASE * angle) / 2.0;
    long targetTicks = (targetArcLength / (PI * WHEEL_DIAMETER)) * TICKS_PER_REV;

    leftEncoder.write(0);
    rightEncoder.write(0);

    if (angle > 0)
    {
        while (abs(rightEncoder.read()) < targetTicks)
        {
            setMotorSpeed(0, speed);
            setMotorSpeed(1, -speed);
        }
    }
    else
    {
        while (abs(leftEncoder.read()) < targetTicks)
        {
            setMotorSpeed(0, -speed);
            setMotorSpeed(1, speed);
        }
    }
    stopMotors();
}

void setup()
{
    pinMode(MOTOR_L_PWM, OUTPUT);
    pinMode(MOTOR_L_DIR1, OUTPUT);
    pinMode(MOTOR_L_DIR2, OUTPUT);
    pinMode(MOTOR_R_PWM, OUTPUT);
    pinMode(MOTOR_R_DIR1, OUTPUT);
    pinMode(MOTOR_R_DIR2, OUTPUT);

    leftEncoder.write(0);
    rightEncoder.write(0);

    Serial.begin(115200);
}

void loop()
{
    updateOdometry();
    scan_360(lidar);
    moveDistance(100, SPEED); // example to try out
    turnAngle(90, SPEED);     // example to try out
}
