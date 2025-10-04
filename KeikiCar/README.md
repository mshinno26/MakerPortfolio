Keiki Car
The Keiki Car is a motorized wheelchair trainer designed to teach children with cerebral
palsy how to use a wheelchair and prove to insurance companies that a real wheelchair will be
both beneficial and operable for the child. I wired and programmed this car. I worked on this
project with four other members of the Assistive Technology club: another programmer, a wirer,
and two fabricators. We acquired the toy car frame through a donation (see KeikiCar_photo1).
We powered the trainer with a 12-volt battery and incorporated a step-down to 9 volts. A
power switch mediates this power supply to the rest of the car. There are two motors, one for
each back wheel, both wired to the same control pins. A singular linear actuator is used to
steer—the front axle is fixed at the center, while the linear actuator pushes one side forward or
backward. The car is equipped with five ultrasonic sensors: three in a head array for forward,
right, and left; and two for proximity sensing in the front and back. The car is also wired to four
buttons, one for each direction. A toggled kill button in the back prevents movement and steering
even when the car is powered, and two switches turn the head array and buttons, respectively, on
or off (see KeikiCar_photo2). A potentiometer sets the maximum speed of the car. All of these
components are controlled through an Arduino Mega, wired through a screw terminal block.
The program for the Arduino board begins by initializing and declaring global variables
such as constant pin numbers and maximum speeds, as well as enumerators for each direction
(see KeikiCar_code). Ultrasonic sensor controls reside in a separate class, where the Arduino
sends commands to and reads updates from the sensor itself, and calculates distances from the
sensor to objects. Two functions to update or calculate dynamic motor and linear actuator speeds
follow the Ultrasonic class. The next function, when called repeatedly, recenters the linear
actuator. Five Ultrasonic objects are declared, one for each sensor. Another function checks
which, if any, senses the closest object within the threshold distance.
The setup() sets input and output pins and initializes the kill button’s status. The loop()
starts by reading the potentiometer to set the maximum speed, and reading the linear actuator’s
position (for proper future writing). Each direction button is then read (if the buttons are turned
off via the switch, their states are automatically set to low), as well as the kill switch. Since the
button has a built-in LED, the program also turns the light on and off (lit for kill, off for
function). Then, given kill switch has not been hit, nested if-statements check the previously
saved direction button states. If the forward or backward button is pressed, the Arduino writes
that direction to the motor. Using the ramp_speed() function, each iteration increases in speed
while the button is still pressed and until the maximum speed is met. If the right or left button is
pressed, the Arduino writes that direction to the linear actuator (one pin is for forward motion,
and one is for backward motion). In addition to this steering, the program treats direction buttons
like the forward button, moving the car forward, unless the backward button is pressed at the
same time, in which case the program moves the car backward. After these buttons are checked,
and if the head array is switched on, the program moves on to the head array, checking the saved
state of each of the three sensors using a switch case. If either the right or left sensor is activated,
the Arduino writes that direction to the linear actuator, until the maximum angle is met; just like
with the directional buttons, the program also moves the car forward (unless the steering is
already at the maximum). If the forward sensor is activated, the program moves the car forward.
For any situation explained thus far in which the car moves forward or backward, the program
checks the corresponding proximity sensor and, if activated, will set the motor to low. If the kill
switch is activated, the program stops the motors and linear actuator; otherwise, if no button or
head array sensor is activated, the program stops the motors and recenters the steering using
recenter().
When building the wheelchair trainer, we had a few issues. Two stand out the most: one
with automatic recentering and one with the forward button. When I first added the recentering
function, it would start jittering in the very center. I deduced that this was because the linear
actuator could never reach the exact middle position, given the distances the program wrote to it.
I fixed this issue by adding a margin of error in which the recentering would cease. However,
when I later added ramping linear actuator speed, it occurred to me that this might no longer be
an issue. The dynamic steering speed function, linacSpeed(), decreases steering speed for
shallow angles, allowing for more precise steering without making sharper turns impossible or
slow. I realized that the slower speed in the middle might allow for exact recentering; after
removing the margin of error in the recentering function, we tested the steering in multiple
corner cases, and it recentered perfectly.
Another issue came when my programming partner changed the structure of the nested
if-statements that check the buttons. While he removed some redundancy, the forward and
backward buttons and head array sensors stopped working. I traced the code and found an issue,
but not with reading the buttons or sensors themselves, as I had expected. Instead, the default
else-statement, intended to turn off the motors and linear actuator (at that time, the recentering
function had not yet been added), was nested in the wrong if-statement, causing the default to run
even when the buttons or sensors were activated. I fixed the issue by moving the else-statement.
