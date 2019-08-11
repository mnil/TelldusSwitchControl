# Telldus Switch Control
Scripts for controlling a Telldus switch by sniffing and playing back the 433MHz signal.

# Prerequisite
The scripts has been tested on a Raspberry Pi 3B+ with RF-link 433MHz receiver and transmitter.

# Installation and setup
Install pigpio by following the instructions on: http://abyz.me.uk/rpi/pigpio/download.html

Make sure the receiver and transmitter and connected to correct GPIO ports, or change the script to reflect your setup.

# Sniffing the code
Start the script with no parameter, `./telldus_switch_ctrl.py`, and press the on button on the telldus remote a couple of times.
After 15 s the most likely signal candidate will be printed, turn the switch off with the remote and try to transmit the on code with `./telldus_switch_ctrl.py S101...101P` which hopefully should turn the switch on.
Do the same procedure for the off button and repeat for the three possible switches.