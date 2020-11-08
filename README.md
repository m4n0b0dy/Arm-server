# The ARM

## Controlling a robotic arm with hand (10 DOF) via OpenPose and PCA9685 Pi programming (and Python ofc)

## Project ToDos
- [x] Robot Arm Built
- [x] Robot Arm Progammable via Pi (was challenging but figured it out)
- [x] OpenPose WebCam succesfully run on Linux Server (also a doozy, thank you Docker)
- [ ] Custom OpenPose Dockerfile for specific use case (build OpenPose and run webcam capture bash / transfer script / set env variable for stream output)
- [ ] Custom PI Dockerfile for receiving instructioins and controlling hand via PCA9685 
- [ ] Orchestration and Documentation

## Project Tools
- Python
  - CV2
  - Flask
  - PCA9685
  - Requests
  - pyinotify
- AI Models
  - OpenPose Hand Model
  - OpenPose Body Model  
- Docker
  - OpenPose Dockerimage (with some customization)
  - Custom Flask API docker for PI

## Publication
- [Not Published yet](keenanvenuti.com/projects)

## Installation and Running
```sh
git clone git@github.com:m4n0b0dy/Arm.git
```
```sh
#on GPU server
sudo docker run
#on PI
sudo docker run
```
