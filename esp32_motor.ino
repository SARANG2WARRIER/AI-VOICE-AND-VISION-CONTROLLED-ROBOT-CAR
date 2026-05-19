// firmware/esp32_motor/esp32_motor.ino
//
// ESP32 Motor + LED Command Receiver
// Reads commands over USB Serial from Raspberry Pi and controls:
//   - L298N motor driver (2 DC motors)
//   - Built-in LED
//
// WIRING (L298N → ESP32):
//   IN1 → GPIO 26    IN2 → GPIO 27   (Left motor)
//   IN3 → GPIO 14    IN4 → GPIO 12   (Right motor)
//   ENA → GPIO 25    ENB → GPIO 13   (PWM speed)
//   LED → GPIO 4
//
// Commands received (newline-terminated):
//   MOVE_FORWARD, MOVE_BACKWARD, TURN_LEFT, TURN_RIGHT, STOP
//   LED_ON, LED_OFF

// ── Pin definitions ───────────────────────────────────────────────────────────
#define IN1  26
#define IN2  27
#define IN3  14
#define IN4  12
#define ENA  25
#define ENB  13
#define LED_PIN 4

#define MOTOR_SPEED 200   // 0-255 PWM

// ── Setup ─────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  stopMotors();
  Serial.println("ESP32 Motor Controller Ready");
}

// ── Main loop ─────────────────────────────────────────────────────────────────
void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    Serial.println("CMD: " + cmd);
    executeCommand(cmd);
  }
}

// ── Command dispatcher ────────────────────────────────────────────────────────
void executeCommand(String cmd) {
  if      (cmd == "MOVE_FORWARD")  moveForward();
  else if (cmd == "MOVE_BACKWARD") moveBackward();
  else if (cmd == "TURN_LEFT")     turnLeft();
  else if (cmd == "TURN_RIGHT")    turnRight();
  else if (cmd == "STOP")          stopMotors();
  else if (cmd == "LED_ON")        digitalWrite(LED_PIN, HIGH);
  else if (cmd == "LED_OFF")       digitalWrite(LED_PIN, LOW);
  else    Serial.println("Unknown: " + cmd);
}

// ── Motor functions ───────────────────────────────────────────────────────────
void moveForward() {
  analogWrite(ENA, MOTOR_SPEED); analogWrite(ENB, MOTOR_SPEED);
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void moveBackward() {
  analogWrite(ENA, MOTOR_SPEED); analogWrite(ENB, MOTOR_SPEED);
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void turnLeft() {
  analogWrite(ENA, MOTOR_SPEED); analogWrite(ENB, MOTOR_SPEED);
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);  // left motor backward
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // right motor forward
}

void turnRight() {
  analogWrite(ENA, MOTOR_SPEED); analogWrite(ENB, MOTOR_SPEED);
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // left motor forward
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);  // right motor backward
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}
