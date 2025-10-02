/**
@author Max Shinno, Daniel Lin
*/

#include <Arduino.h>
//Joystick Setup
#define VRXPIN A0
#define VRYPIN A1

#define LinacA 48
#define LinacB 46
#define LinacPosPin A3
#define ENA 12


//back and front proximity sensors
#define UltraFrontTrig 49
#define UltraFrontEcho 51

#define UltraBackTrig 45
#define UltraBackEcho 47

//Head array sensors
#define ultra_left_trig 22
#define ultra_left_echo 23

#define ultra_right_trig 24
#define ultra_right_echo 25

#define ultra_back_trig 32
#define ultra_back_echo 33
//control panel
#define UltrasonicButton 28  //ultra toggle
#define HeadArrayButton 30
#define Potentiometer A14     //motor speed
//kill switch
#define StopButton 29
#define StopLED 2

#define ForwardButton 35
#define RightButton 37
#define LeftButton 39
#define BackButton 41

#define motor1a 9
#define motor1b 8

#define LinacUpperLimit 380
#define LinacLowerLimit 220
#define LinacMidLow 298
#define LinacMidHigh 302
#define maxLinacSpeed 255

int RealLinacPos;

//Ultrasonic Setup

int ProxFront;
long duration1;
int distance1;

int ProxBack;
long duration2;
int distance2;

int Forward;
int Right;
int Left;
int Back;

int ButtonMotorSpeed = 10;

enum head_array_state {
  LEFT,
  RIGHT,
  FRONT,
  NONE
} ;

//Killswitch Setup
int PreviousStopButtonState;
int CurrentStopButtonState;
int StopStatus;
// int StopLED = 37;

int xRestMin;
int xRestMax;
int LinacRestMax;
int LinacRestMin;
int LinacExtendMax;
int LinacExtendMin;

int yRestMin;

int yRestMax;

// unsigned long t0;
// unsigned long elapsed;


class Ultrasonic {
private:
  byte echo_pin;
  byte trigger_pin;
  float duration;
  int distance;
  head_array_state state;
public:
  Ultrasonic(byte e_pin, byte t_pin, head_array_state s_state) {
    echo_pin = e_pin;
    trigger_pin = t_pin;
    state = s_state;
    init();
  }

  void init() {
    pinMode(echo_pin, INPUT);
    pinMode(trigger_pin, OUTPUT);
    update();
  }

  int update() {
    
    digitalWrite(trigger_pin, LOW);
    // digitalWrite(echo_pin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds

    digitalWrite(trigger_pin, HIGH);
    // digitalWrite(echo_pin, HIGH);
    delayMicroseconds(10);

    digitalWrite(trigger_pin, LOW);
    // digitalWrite(echo_pin, LOW);
    delayMicroseconds(10);


    duration = pulseIn(echo_pin, HIGH, 10000);
    //duration2 = pulseIn(UltraBackEcho, HIGH);
    // Reads the echoPin, returns the sound wave travel time in microseconds

    // Calculating the distance
    distance = duration * 0.034 / 2;

    if (distance == 0) {
      distance = 1000;
    }

    return distance;
    delay(100);
  }

  int get_dist() {
    return distance;
  }

  head_array_state get_state() {
    return state;
  }

  
  bool check_prox() {
    if (digitalRead(UltrasonicButton) == HIGH) {
        return update() > 30;
    } else {
      return true;
    }
  }

  bool check_head_array() {
    if (digitalRead(HeadArrayButton) == HIGH) {
      return update() > 30;
    } else {
      return true;
    }
  }
};

void ramp_speed(int maxSpeed) {
  if (ButtonMotorSpeed < maxSpeed) {
    ButtonMotorSpeed += 5;
  }
}

int linacSpeed(int pos) {
  if (pos < LinacMidLow - 15) {
    return maxLinacSpeed;
  } else if (pos < LinacMidLow) {
    return maxLinacSpeed/2;
  } else if (pos > LinacMidHigh + 15) {
    return maxLinacSpeed;
  } else if (pos > LinacMidHigh) {
    return maxLinacSpeed/2;
  }
}

int recenter(int pos) {
  if (pos < LinacMidLow) {
    analogWrite(LinacA, linacSpeed(pos));
    digitalWrite(LinacB, LOW);
  } else if (pos > LinacMidHigh) {
    analogWrite(LinacB, linacSpeed(pos));
    digitalWrite(LinacA, LOW);
  } else {
    digitalWrite(LinacA, LOW);
    digitalWrite(LinacB, LOW);
  }
}

Ultrasonic ultra_front(UltraFrontEcho, UltraFrontTrig, NONE);
Ultrasonic ultra_back(UltraBackEcho, UltraBackTrig, NONE);
Ultrasonic ultra_left(ultra_left_echo, ultra_left_trig, LEFT);
Ultrasonic ultra_right(ultra_right_echo, ultra_right_trig, RIGHT);
Ultrasonic head_ultra_back(ultra_back_echo, ultra_back_trig, FRONT);


Ultrasonic head_array[] = {ultra_left, ultra_right, head_ultra_back};


head_array_state check_head_array() {
  head_array[0].update();
  head_array[1].update();
  head_array[2].update();

  int min_value = min(min(head_array[0].get_dist(), head_array[1].get_dist()), head_array[2].get_dist());

  if (min_value >= 30 || min_value == 0) {
    return NONE;
  } else {
    for (int i = 0; i <= 2; i++) {
      if (min_value == head_array[i].get_dist()) {
        return head_array[i].get_state();
      }
    }
    return NONE;
  }
}

void setup() {
  //Motors
  pinMode(motor1a, OUTPUT);
  pinMode(motor1b, OUTPUT);

  //Linear Actuator
  pinMode(LinacA, OUTPUT);
  pinMode(LinacB, OUTPUT);
  pinMode(LinacPosPin, INPUT);

  //Ultrasonic Sensors
  pinMode(UltraFrontTrig, OUTPUT);
  pinMode(UltraFrontEcho, INPUT);

  pinMode(UltraBackTrig, OUTPUT);
  pinMode(UltraBackEcho, INPUT);

  pinMode(ultra_left_echo, INPUT);
  pinMode(ultra_left_trig, OUTPUT);

  pinMode(ultra_right_echo, INPUT);
  pinMode(ultra_right_trig, OUTPUT);

  pinMode(ultra_back_echo, INPUT);
  pinMode(ultra_back_trig, OUTPUT);

  pinMode(UltrasonicButton, INPUT);
  pinMode(HeadArrayButton, INPUT);


  //Misc
  pinMode(Potentiometer, INPUT);

  //Killswitch
  pinMode(StopButton, INPUT);
  pinMode(StopLED, OUTPUT);
  StopStatus = 0;

  //Buttons
  pinMode(ForwardButton, INPUT);
  pinMode(RightButton, INPUT);
  pinMode(LeftButton, INPUT);
  pinMode(BackButton, INPUT);
}


void loop() {
//   t0 = micros();
//   loop logic
//   elapsed = micros() - t0;
//   Serial.println(elapsed);

  //Changing Values;

  int MaxMotorSpeed = map(analogRead(Potentiometer), 0, 1023, 25, 300);  //last number value is max motor speed


  RealLinacPos = analogRead(LinacPosPin);
  // Serial.print("Linear Atuator Position:");

  //Serial.println(NegativeyValue);
  
 


  Forward = digitalRead(ForwardButton);
  Back = digitalRead(BackButton);
  Left = digitalRead(LeftButton);
  Right = digitalRead(RightButton);

  

  //Estop
  PreviousStopButtonState = CurrentStopButtonState;
  CurrentStopButtonState = (digitalRead(StopButton));

  if ((CurrentStopButtonState == 1) && (PreviousStopButtonState == 0)) {
    if (StopStatus == 0) {
      StopStatus = 1;
    } else if (StopStatus == 1) {
      StopStatus = 0;
    }
  }
  if (StopStatus == 1) {
    digitalWrite(StopLED, HIGH);
  } else if (StopStatus == 0) {
    digitalWrite(StopLED, LOW);
  }

  if (StopStatus == 0) {
    if (Forward == HIGH && ultra_front.check_prox()) {
        ramp_speed(MaxMotorSpeed);
        analogWrite(motor1a, ButtonMotorSpeed);
        digitalWrite(motor1b, LOW);  //WIP
    } else if (Right == HIGH && !Back) {
      if (RealLinacPos < LinacUpperLimit) {
        digitalWrite(LinacA, HIGH);
        digitalWrite(LinacB, LOW);
      }
      if (ultra_front.check_prox()) {
        ramp_speed(MaxMotorSpeed);
        analogWrite(motor1a, ButtonMotorSpeed);
        digitalWrite(motor1b, LOW);
      } else {
        digitalWrite(motor1a, LOW);
        digitalWrite(motor1b, LOW);
      }
    } else if (Left == HIGH && !Back) {
      if (RealLinacPos > LinacLowerLimit) {
        digitalWrite(LinacB, HIGH);
        digitalWrite(LinacA, LOW);
      }
      if (ultra_front.check_prox()) {
        ramp_speed(MaxMotorSpeed);
        analogWrite(motor1a, ButtonMotorSpeed);
        digitalWrite(motor1b, LOW);
      } else {
        digitalWrite(motor1a, LOW);
        digitalWrite(motor1b, LOW);
      }
    } else if (Right == HIGH) {
      if (RealLinacPos < LinacUpperLimit) {
        digitalWrite(LinacA, HIGH);
        digitalWrite(LinacB, LOW);
        ramp_speed(MaxMotorSpeed);
      }
      if (ultra_back.check_prox()) {
        digitalWrite(motor1a, LOW);
        analogWrite(motor1b, ButtonMotorSpeed);
      } else {
        digitalWrite(motor1a, LOW);
        digitalWrite(motor1b, LOW);
      }
    } else if (LEFT == HIGH) {
      if (RealLinacPos > LinacLowerLimit) {
        digitalWrite(LinacB, HIGH);
        digitalWrite(LinacA, LOW);
      }
      if (ultra_back.check_prox()) {
        ramp_speed(MaxMotorSpeed);
        digitalWrite(motor1a, LOW);
        analogWrite(motor1b, ButtonMotorSpeed);
      } else {
        digitalWrite(motor1a, LOW);
        digitalWrite(motor1b, LOW);
      }
    } else if (Back == HIGH && (ultra_back.check_prox())) {
      ramp_speed(MaxMotorSpeed);
      digitalWrite(motor1a, LOW);
      analogWrite(motor1b, ButtonMotorSpeed);
    } else if (digitalRead(HeadArrayButton) == HIGH) {
      switch(check_head_array()) {
        case LEFT:
          if (RealLinacPos > LinacLowerLimit) {
            digitalWrite(LinacB, HIGH);
            digitalWrite(LinacA, LOW);
          } else {
            digitalWrite(LinacB, LOW);
            digitalWrite(LinacA, LOW);
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
          }
          if (ultra_front.check_prox()) {
            analogWrite(motor1a, ButtonMotorSpeed);
            digitalWrite(motor1b, LOW);
          } else {
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
          }
          break;
        case RIGHT:
          if (RealLinacPos < LinacUpperLimit) {
            digitalWrite(LinacA, HIGH);
            digitalWrite(LinacB, LOW);
          } else {
            digitalWrite(LinacB, LOW);
            digitalWrite(LinacA, LOW);
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
          }
          if (ultra_front.check_prox()) {
            analogWrite(motor1a, ButtonMotorSpeed);
            digitalWrite(motor1b, LOW);
          } else {
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
          }
          break;
        case FRONT:
          if (ultra_front.check_prox()) {
            ramp_speed(MaxMotorSpeed);
            analogWrite(motor1a, ButtonMotorSpeed);
            digitalWrite(motor1b, LOW);
          } else {
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
          }
          recenter(RealLinacPos);
          break;
        case NONE:
          digitalWrite(motor1a, LOW);
          digitalWrite(motor1b, LOW);
          recenter(RealLinacPos);
          ButtonMotorSpeed = 25;
          break;
        }
    } else {
      digitalWrite(motor1a, LOW);
      digitalWrite(motor1b, LOW);
      recenter(RealLinacPos);
      ButtonMotorSpeed = 25;
    }
  } else {
    digitalWrite(motor1a, LOW);
    digitalWrite(motor1b, LOW);
    digitalWrite(LinacA, LOW);
    digitalWrite(LinacB, LOW);
    ButtonMotorSpeed = 25;
  }


  // Send MaxMotorSpeed, Head Array Status, Prox,  
  delay(100);
}