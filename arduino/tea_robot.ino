#include <Servo.h>

#define CONVEYOR_MOVE_TIME 380
#define KETTLE_POUR_TIME 3500
#define EXTRACT_TIME 10000

#define CONVEYOR_MOTOR_NUM 3






// ------ Lift -------
Servo lift_servo;
const int lift_servo_pin = 7;

void lift_down() {
  lift_servo.write(140);
}

void lift_up() {
  lift_servo.write(20);

}




// ---- Kettle -----
const int kettle_pin = 8;

void kettle_pour(int wait_time) {
  digitalWrite(kettle_pin, HIGH);
  delay(wait_time);
  digitalWrite(kettle_pin, LOW);
}


// ---- Conveyor ----
const int conveyor_motors[CONVEYOR_MOTOR_NUM][2] = {
  {22, 23},
  {24, 25},
  {26, 27}
};

void drop_teabag(int tea_num) {
  digitalWrite(conveyor_motors[tea_num][0], LOW);
  digitalWrite(conveyor_motors[tea_num][1], HIGH);
  delay(CONVEYOR_MOVE_TIME);
  digitalWrite(conveyor_motors[tea_num][0], LOW);
  digitalWrite(conveyor_motors[tea_num][1], LOW);
}



// ------ Combined all --------
void serve_tea(int tea_num) {
  lift_down();
  drop_teabag(tea_num);
  kettle_pour(KETTLE_POUR_TIME);
  delay(EXTRACT_TIME);
  lift_up();

}


void setup() {
  for (int i = 0; i < CONVEYOR_MOTOR_NUM; i++) {
    pinMode(conveyor_motors[i][0], OUTPUT);
    pinMode(conveyor_motors[i][1], OUTPUT);
    digitalWrite(conveyor_motors[i][0], LOW);
    digitalWrite(conveyor_motors[i][1], LOW);
  }
  pinMode(kettle_pin, OUTPUT);
  digitalWrite(kettle_pin, LOW);
  lift_servo.attach(lift_servo_pin);
  pinMode(lift_servo_pin, OUTPUT);
  lift_servo.write(20);
  Serial.begin(9600);
}

void loop() {

  String str;
  if (Serial.available() > 0) {
    str = Serial.readString();
    str.trim();

    if (str == "serve_tea1") {
      serve_tea(0);
    }
    if (str == "serve_tea2") {
      serve_tea(1);
    }
    if (str == "serve_tea3") {
      serve_tea(2);
    }
    if (str == "up") {
      lift_up();

    }
    if (str == "down") {
      lift_down();
    }
  }
}

