# The Server

## Extracing Hand and Body movement via OpenPose and translating into [Robot Arm](https://github.com/m4n0b0dy/Arm-robot) commands

## Project ToDos
- [x] OpenPose WebCam succesfully run on Linux Server
- [x] Python code developed to convert 3d OpenPose coordinates into Arm Servo commands
- [x] Python code developed to read stream of OpenPose demo output and call Arm API
- [x] Custom OpenPose Dockerfile for specific use case
- [x] Enable Docker usage of network, display, and webcam
- [ ] Revisit inverse kinematics equations for refined movement

## Project Tools
- Python
  - CV2
  - Requests
  - pyinotify
- AI Models
  - OpenPose Hand Model
  - OpenPose Body Model
- Docker base images
  - OpenPose

## The Video
- [Video Published Here](linkedin.com)

## Installation and Running
```sh
git clone git@github.com:m4n0b0dy/Arm-server.git
docker build -t myopenpose .
sudo xhost + 
docker run --network="host" -e DISPLAY --privileged --gpus all --device=/dev/video0 --name myopenpose -it myopenpose:latest
```
### Then with docker image built, we can run code specific to the use case
#### To run the finger detection, the following works best
```sh
./build/examples/openpose/openpose.bin --write_json output/ --hand
python3 deploy/file_stream.py
```
#### To run the wrist/arm detection, it's best to normalize accordingly
```sh
./build/examples/openpose/openpose.bin --write_json output/ --hand --keypoint_scale 4
python3 deploy/file_stream.py
```
##### To improve/fine tune the readings of your hand/arm please read through IK_SOLVER.py as it holds the inverse kinematics logic (what determines movement from coordinates)

## Server Specs
- GPU: Nvidia 1660 Super
- CPU: Intel E5-1620 3.6GHz 4-Core
- RAM: 32GB DDR3
- [Webcam](https://www.amazon.com/gp/product/B088H1QLRN/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
