#include <Servo.h>

Servo liftServo;
Servo gripServo;

const int LIFT_PIN = 9;
const int GRIP_PIN = 10;

const int ANGLE_LOWER = 30;
const int ANGLE_RAISE = 120;
const int ANGLE_GRAB  = 40;
const int ANGLE_OPEN  = 110;

void setup() {
  Serial.begin(9600);

  liftServo.attach(LIFT_PIN);
  gripServo.attach(GRIP_PIN);

  liftServo.write(ANGLE_RAISE);
  gripServo.write(ANGLE_OPEN);

  Serial.println("Ready. Commands: 1 - lower, 2 - raise, 3 - grab, 4 - release");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '\n' || command == '\r' || command == ' ') {
      return;
    }

    switch (command) {
      case '1':
        liftServo.write(ANGLE_LOWER);
        Serial.print("Lowering (angle ");
        Serial.print(ANGLE_LOWER);
        Serial.println(" deg.)");
        break;

      case '2':
        liftServo.write(ANGLE_RAISE);
        Serial.print("Raising (angle ");
        Serial.print(ANGLE_RAISE);
        Serial.println(" deg.)");
        break;

      case '3':
        gripServo.write(ANGLE_GRAB);
        Serial.print("Grabbing (angle ");
        Serial.print(ANGLE_GRAB);
        Serial.println(" deg.)");
        break;

      case '4':
        gripServo.write(ANGLE_OPEN);
        Serial.print("Releasing (angle ");
        Serial.print(ANGLE_OPEN);
        Serial.println(" deg.)");
        break;

      default:
        Serial.println("Unknown command. Enter 1, 2, 3, or 4.");
        break;
    }
  }
}
