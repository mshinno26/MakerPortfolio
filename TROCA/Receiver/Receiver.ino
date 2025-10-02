/**
@author Max Shinno
*/

// serial, radio, and servo libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

// transceiver pins, radio constructor
const int csn_pin = 8;
const int ce_pin = 7;
RF24 radio(ce_pin, csn_pin);

// will store output received
int button;

// channel matches with transmitter
const byte address[6] = "00001";

// feeder servo constructor, servo pins, angle constants
Servo feeder;
const int servoPin1 = 6;
const int open1 = 135;
const int closed1 = 45;

// mixer servo constructor, servo pins, angle constants
Servo mixer;
const int servoPin2 = 5;
const int open2 = 145;
const int closed2 = 75;

void setup() {
  // set up radio; address 00001, pipe 0, minimum power level, set as receiver
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();

  // set feeder servo pin, move to default position
  feeder.attach(servoPin1);
  feeder.write(closed1);
  // allow servo time to move
  delay(500);
  // detach to prevent rewriting
  feeder.detach();
  // set mixer servo pin, move to default position
  mixer.attach(servoPin2);
  mixer.write(closed2);
  // allow servo time to move
  delay(500);
  mixer.detach();
}

void loop() {
  // check for unread transmission
  if (radio.available()) {
    // read transmission into "button" int
    radio.read(&button, sizeof(button));

    // when button pressed
    if (button) {
      // open and close feeder and mixer; delay 0.5 seconds to allow each part to move
      move(mixer, servoPin2, open2, closed2);
      move(feeder, servoPin1, open1, closed1);
    }
  }
}

void move(Servo servo, int pin, int open, int closed) {
  // open and close param servo; delay 0.5 seconds to allow each part to move
  servo.attach(pin);
  servo.write(open);
  delay(500);
  servo.write(closed);
  delay(500);
  servo.detach();
}