/**
@author Max Shinno
*/

// include serial and radio libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// radio pins and constructor
const int ce_pin = 7;
const int csn_pin = 8;
RF24 radio(ce_pin, csn_pin);

// to store output of RF24.write(): true if received acknowledgement of transmisison, false otherwise
bool success;

// button pin, light pin; var to store output of digitalRead() of button
const int buttonPin = 3;
const int ledPIN = 5;
int buttonState;
int prevState = false; // to store last state of button, preventing resending when holding

// address matches receiver
const byte address[6] = "00001";

void setup() {
  // set button pin input and led pin output; transmitter pins handled automatically by library
  pinMode(buttonPin, INPUT);
  pinMode(ledPIN, OUTPUT);
  digitalWrite(ledPIN, HIGH);
  // set up radio; address 00001, automatically writes to pipe 0, power level minimum, set as transmitter
  success = radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  // read button input pin; HIGH if pressed, LOW otherwise
  buttonState = digitalRead(buttonPin);
  // send message if button pressed & wasn't previously pressed
  if (buttonState && !prevState) {
    prevState = HIGH;
    success = radio.write(&buttonState, sizeof(buttonState));
    // if received acknowledgement, temporarily turn off LED, and delay, allowing servo to move before resending
    if (success) {
      digitalWrite(ledPIN, LOW);
      delay(2000);
      digitalWrite(ledPIN, HIGH);
    }
  } else if (!buttonState && prevState) {
    prevState = LOW;
  }
  // wait 0.1 seconds to prevent overloading board
  delay(100);
}