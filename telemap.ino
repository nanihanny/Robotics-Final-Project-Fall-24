#include "motor_encoder.ino"
#include "my_lidar.ino"

void setup()
{
    setupMotors();
    lidar.begin(Serial);
    pinMode(RPLIDAR_MOTOR, OUTPUT);
    analogWrite(RPLIDAR_MOTOR, 255);
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available())
    {
        char command = Serial.read();
        handleKeyboardCommand(command);
    }
    updateLidarAndMap();
}

void handleKeyboardCommand(char command)
{
    switch (command)
    {
    case 'w':
        moveDistance(10, SPEED);
        break;
    case 's':
        moveDistance(-10, SPEED);
        break;
    case 'a':
        turnAngle(-30, SPEED);
        break;
    case 'd':
        turnAngle(30, SPEED);
        break;
    case 'q':
        stopMotors();
        break;
    }
}

void updateLidarAndMap()
{
    if (IS_OK(lidar.waitPoint()))
    {
        float distance = lidar.getCurrentPoint().distance;
        float angle = lidar.getCurrentPoint().angle;

        if (distance > 0)
        {
            update_local_map(angle, distance);
        }
    }
}
