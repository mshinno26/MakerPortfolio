TROCA machine
The Tangible Reinforcement Operant Condition Audiometry (TROCA) machine is meant
for children with disabilities who may not understand how to respond in an audiometry test. The
machine includes a remote that an audiometrist activates when the patient does something
correctly, as well as a large receptacle of toy capsules that releases one ball at a time (see
TROCA_video). I designed, wired, and programmed this machine. I worked on this project with
two other members of the Assistive Technology club: a wirer and a fabricator.
We powered the remote with a 9-volt battery; a switch mediates this battery and the rest
of the components. The remote houses a single button with a built-in LED (connected to ground
and control pins through resistors), as well as an nRF24L01 transceiver (see
TROCA_Transmitter_photo). These components are wired to an Arduino Nano ESP32 through a
breadboard. The housing for the remote is a work-in-progress; the next version will be larger,
with enough space to fit the components better, and a button cap instead of the LED sticking out
from the top. The main machine is powered by a wall outlet, but also has the option to be
powered with a 9-volt battery. The TROCA machine houses two servos and a transceiver, as well
as capacitors to smooth out changes in power draw from these components (see
TROCA_Receiver_photo). The housing for the balls is shaped like a funnel, with modular walls
to increase the capacity when needed. One servo extends through a hole in the funnel, knocking
balls into the funnel’s outlet. The other servo blocks the outlet until the button is pressed, in
which case it moves out of the way to let the ball drop, then swings it to the ramp. These
components are wired to an Arduino Mega through a screw terminal block.
The program for the remote transmitter’s Nano board begins by including libraries (to
allow communication with the transceiver), and initializing/declaring pins, an RF24 object, and
variables (see TROCA_Transmitter_code). Before the setup(), the program sets the address for
the transceiver (a 6-byte code that, while arbitrary, must be equal to that of the receiver). The
setup() assigns input and output pins, sets up the RF24, and stops the transceiver to prevent
unnecessary power usage. It also turns on the button’s LED to let the user know that the remote
is ready to go. Every loop(), the Nano reads the state of the button; if it is pressed, it sends a
signal to the main machine’s RF24. If the remote receives an acknowledgement, it pauses to
prevent additional button presses while the TROCA machine’s servos are moving. During the
delay, the program turns off the LED to inform the user that the transceivers’ communication
worked, and that pressing the button will do nothing until it turns back on. The program also
includes a status variable for the button, so that holding the button does not activate the
transceiver multiple times; the user must let go of the button and press it again to send the signal.
The program for the main receiver’s Mega board begins by including the same RF24
libraries, as well as a Servo control library, and initializing/declaring pins, global objects, and
constants (see TROCA_Receiver_code). The setup() sets up the transceiver and both servos,
including setting the radio as a receiver, attaching pins, and writing default servo positions.
Every loop() iteration, the program checks for unread transceiver messages. When the radio
receives a transmission, the program checks it for the button state—if it is high (as it always
should be), it calls the move function on the mixer servo, then the feeder servo. The move()
function writes to the servo, and takes as parameters the servo object, its control pin, and the
positions to which the servo should move.
One issue we faced was with the transceivers—they’d start working, but soon stop
communicating. My first thought was to simplify the transmitter code to allow the transceiver to
send signals only when the button is initially pressed, rather than sending constant updates on the
button’s state. This alleviated the issue, but didn’t fix it entirely. So, I tried some other solutions,
the most notable of which was the addition of resistors, but to no effect; we later completely
ruled out this solution due to the manufacturer’s indication that the transceiver was built for up to
23 volts of power, well above the possible power. So, I did some research and found that
transceivers can be quite inconsistent with power draw. I added capacitors over the 3-volt power
and ground buses (there was already one for the servo on the 5-volt bus), solving the issue.
Two more issues were that the balls would not fall properly into the outlet of the funnel,
and the balls were not big enough (see TROCA_Prototype_video). We solved the first problem
with the second servo, which knocked the balls into the hole at the bottom of the funnel. We
solved the second problem by scaling up the entire receiver machine, so that the receptacle
would fit larger balls, and the balls could fit objects inside.
Another significant issue we came across was that the servos buzzed, even when not in
use. Normally, this would not be so much of a problem. However, since this is an audiometry
machine, it is used in booths that must be silent. I tried a few solutions, the first of which was
moving only one servo at a time; while this helped, it did not entirely solve the problem (we
eventually kept this functionality to protect the board, since Megas aren’t exactly built to power
two servos at once anyway). My teammate sanded the opening in the funnel for the servo to
prevent friction and strain, but this did not fix the issue either. Realizing that buzzing was only an
issue when the servo wasn’t moving, I added transistors as a low-side switch for the Servo’s
ground pin; in this way, power would not run through the ground pin when it wasn’t necessary.
However, this solution provided inconsistent results in our tests. I did some research and found
that servo pins continue to send signals to keep servos in place, even while the program is not
calling write(). This information deprecated the low-side switch solution (it’s unsafe to cut off
ground to the servo while writing signals to it), but also inspired a new solution. The only way to
completely cut communication through the control pin is to detach() the servo, so I decided to
detach and re-attach before and after moving each servo. This solved the problem, suggesting
that there was most likely an issue with continued signals through the control pin.
A third issue was with our PWB (originally used in the remote, instead of the
breadboard). For some reason, some buses on our printed wiring board (PWB) did not connect
properly. I tried swapping out the board and re-soldering our jumper wires, but these solutions
did not work. The remote needed these buses to connect multiple components in series, such as
wires and resistors, so it was not possible to simply remove the PWB—instead, we replaced it
with a breadboard. This was not the most ideal scenario, since breadboards can be unreliable
when it comes to keeping jumper wires connected, and soldering is not possible on a plastic
board. However, this remote will not be jostled too much (far less than the Keiki Car, for
example), and the housing is built snugly, so the breadboard does not reduce functionality.
