# TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition

This project focuses on extracting information from a drone's video feed regarding ArUco codes and saving the data to a CSV file. The specific data points we aimed to extract are:

    - The ArUco code number detected in the video.
    - The 2D coordinates of the ArUco code corners.
    - The yaw (rotation) of the drone.
    - The distance between the drone and the ArUco code.

## How to Use


Ensure you have the required libraries installed by checking the requirements.txt file.


## Running the Project

To run the project, use the following commands:

```sh
git clone https://github.com/Autonomous-robots-robota/TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition.git
run detect_aruco_on_video.py
```


## Project Implementation

In this project, we utilized OpenCV's built-in functions for image recognition of ArUco codes. The process involved the following steps:

```sh

   1. Video Processing: We looped through each frame of the video.
   2. ArUco Code Detection: For each frame, we used cv2.aruco.detectMarkers to detect ArUco codes.
   3. Data Extraction:
      3.1 When an ArUco code was detected, we extracted the corners and the marker ID (ArUco name).
      3.2 For each detected marker ID
          3.2.1 we used cv2.aruco.estimatePoseSingleMarkers get information aboit the drone.
          3.2.2 we used that information to calculate the distance from the drone to the ArUco code, and the yaw of the drone.
          3.2.3 Data Storage: All the extracted information was added to the CSV file (row by row).

```

To ensure accurate results, we used the camera's calibration information, which can be found [here](https://tellopilots.com/threads/camera-intrinsic-parameter.2620/). 


## visuals


https://github.com/Autonomous-robots-robota/TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition/blob/main/aruco_detection_results_challengeB2.mp4
