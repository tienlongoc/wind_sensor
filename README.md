# wind_sensor
my balcony wind sensor project

arduino folder to be run on arduino

processing folder contains processing IDE script that can be run on my PC to read arduino output. Unfortunately couldn't get this to work on raspberry pi. Installed oracle java 8 according to https://askubuntu.com/questions/56104/how-can-i-install-sun-oracles-proprietary-java-jdk-6-7-8-or-jre, and installed processing-3.5.3 for linux 32 bit, but I still can't get the .pde script to run either on processing GUI or in headless mode.

so instead I'll use pyserial on raspberry pi to read arduino output. Funnily I didn't pick this initially just because it wasn't working on my main PC, I couldn't detect the right USB port there, but it's working on my arduino.

use raspberry scripts to scp processing output to my google cloud. Find a way to run this on raspberry pi start up

use gcp files to process the received log files, and make the data available on API. Set up auto emailing mechanism


why don't we just output from arduino once per minute, and then just post directly from python. no need to post the python output log
