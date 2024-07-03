# TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition

<b> This project has two parts </b>

## Part 1

This part of the project focuses on extracting information from a drone's video feed regarding ArUco codes and saving the data to a CSV file. The specific data points we aimed to extract are:

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

For this part of the project, we utilized OpenCV's built-in functions for image recognition of ArUco codes. The process involved the following steps:

```sh

   1. Video Processing: We looped through each frame of the video.
   2. ArUco Code Detection: For each frame, we used cv2.aruco.detectMarkers to detect ArUco codes.
   3. Data Extraction:
      3.1 When an ArUco code was detected, we extracted the corners and the marker ID (ArUco name).
      3.2 For each detected marker ID
          3.2.1 we used cv2.aruco.estimatePoseSingleMarkers get the translation and rotation vectors of the markers.
          3.2.2 we used the translation vectors to calculate the distance from the drone to the ArUco code.
          3.2.3 we used the rotation and traslation vectors to calculate the yaw of the drone.
          3.2.4 Data Storage: All the extracted information was added to the CSV file (row by row).

```

deeper explanation of step 3.2.3:

we used cv2.Rodrigues to calculate the rotation matrix from the rotation vectors.

$RiotationMatrix=cv2.Rodrigues(rotaionVectors​)$

we used the rotation matrix with the translation vectots to calculate the camaras position.

$cameraPos=−RiotationMatrix^T*​translationVectors^T$

we used the camaras position to calculate the yaw of the drone:

$yaw=np.arctan2{(cameraPos[0],cameraPos[2])}*{\frac{π}{180}}$ 



To ensure accurate results, we used the camera's calibration information, which can be found [here](https://tellopilots.com/threads/camera-intrinsic-parameter.2620/). 


## visuals
example of ArUco detection: 
https://www.youtube.com/watch?v=dc078VS6JY

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Fdc078VS6JY/0.jpg)](https://www.youtube.com/watch?v=dc078VS6JY)

example of ArUco detection on video from camera on TelloAI
<img src="https://github.com/Autonomous-robots-robota/TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition/blob/main/img2.jpeg" width=50% height=50%>

___________________________________________________________________________________________
## part 2

This part of the project focuses on taking a still image or a frame from a video and positiong a drone where the image/still was taken from.

## How to Use


Ensure you have the required libraries installed by checking the requirements.txt file.


## Running the Project

To run the project, use the following commands:

```sh
git clone https://github.com/Autonomous-robots-robota/TelloAI-V.0.1---Indoor-Autonomous-Drone-Competition.git
run detect_aruco_on_video.py
then run part2.py
```

## Project Implementation

For this part of the project, we used the First part of the project to get a csv file of a video and randomly choose a frame.

Then, we opened up the computers camera or connected to a phone camera using the [IP WebCam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US) app.

We used the same opencv lbraries as part 1, to see it there are any aruco codes in the video.

If so we checked if the code we are seeing is in the frame we randomly choose.

If so we first corrected the distance to the aruco code moving forward-backwards.

Then we fixed the X and Y axis in the frame moving left-right and up-down.

Finally we fixex the yaw be moving yaw_left-yaw_right.


### deeper explanation

For each variable we calculated the valuein the original frame and in the current frame.

We subtracted the orignal vaue from the current values. If the difference was bigger than a certain eps we mvd the camera accordingly.

we used 3 different eps values. eps_dist, eps_x_y, eps_yaw.

The smaller the eps are the closer the drone can get to being in its original posioning.

To calulate the X Y we used the 2D corners and calculated the avarge x and y from the top left and bottom rght corners.



