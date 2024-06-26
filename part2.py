import cv2
import numpy as np
import pandas as pd
import json
import csv
import time


def pick_aruco_from_csv(file):
    file_path = file  # Update this with the actual path
    data = pd.read_csv(file_path)
    frame = 15
    row = data.loc[data["Frame ID"] == frame]
    return row


def find_aruco(frame, row):
    eps = 100

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

    # Initialize the detector parameters using default values
    parameters = cv2.aruco.DetectorParameters()

    # Camera calibration parameters (example values, replace with your actual calibration results)
    camera_matrix = np.array(
        [[921.170702, 0.000000, 459.904354], [0.000000, 919.018377, 351.238301], [0.000000, 0.000000, 1.000000]])
    dist_coeffs = np.array([-0.033458, 0.105152, 0.001256, -0.006647, 0.000000])

    # Define the real-world coordinates of the ArUco marker corners
    marker_length = 1.0  # Length of a marker's side

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the grayscale image
    corners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If markers are detected, process them
    if markerIds is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)

        for i in range(len(markerIds)):
            print(int(markerIds[i]))
            print(int(row['QR ID'].values[0]))
            if (int(markerIds[i]) == int(row['QR ID'].values[0])):

                # Get the 2D corner points
                first_corners = corners[i].reshape(4, 2).tolist()

                # Calculate distance to the camera
                first_dist = np.linalg.norm(tvecs[i])

                # Calculate yaw angle with respect to the camera "lookAt" point
                rmat, _ = cv2.Rodrigues(rvecs[i])
                camera_pos = -np.matrix(rmat).T * np.matrix(tvecs[i]).T
                yaw_first = np.arctan2(camera_pos[0][0], camera_pos[2][0]) * 180 / np.pi
                yaw_first = float(yaw_first[0][0])

                # calc difference of first corner

                second_corners = eval(row['QR 2D'].values[0])

                # Compute x y distance
                delta_x = first_corners[0][0] - second_corners[0][0]
                delta_y = first_corners[0][1] - second_corners[0][1]

                # Extract and compute angle differences

                yaw_second = row['QR 3D: yaw'].values[0]
                delta_yaw = yaw_first - yaw_second

                # compute move forward or backward

                second_dist = row['QR 3D: dist'].values[0]
                delta_dist = first_dist - second_dist

                # fix left right
                if np.abs(delta_x) > eps:
                    if delta_x > 0:
                        print('move right', 'delt_x = ', delta_x)
                    elif delta_x < 0:
                        print('move left', 'delt_x = ', delta_x)
                # fix up down
                elif np.abs(delta_x) <= eps and np.abs(delta_y) > eps:
                    if delta_y > 0:
                        print('move up', 'delt_y = ', delta_y)
                    elif delta_y < 0:
                        print('move down', 'delt_y = ', delta_y)
                # fix dist
                elif np.abs(delta_x) <= eps and np.abs(delta_y) <= eps and np.abs(delta_dist) > eps:
                    if delta_dist > 0:
                        print('move forward', 'delt_dist = ', delta_dist)
                    elif delta_dist < 0:
                        print('move backward', 'delt_dist = ', delta_dist)
                # fix yaw
                elif np.abs(delta_x) <= eps and np.abs(delta_y) <= eps and np.abs(delta_dist) <= eps and np.abs(
                        delta_yaw) > eps:
                    if delta_yaw > 0:
                        print('yaw right', 'delt_yaw = ', delta_yaw)
                    elif delta_yaw < 0:
                        print('yaw left', 'delt_yaw = ', delta_yaw)

                else:
                    print("you are less then", eps, "away from target position in all directions")

                time.sleep(2)


def open_camera_start_look(row):
    # import the opencv library
    import cv2

    # define a video capture object
    vid = cv2.VideoCapture(0)

    while (True):

        ret, frame = vid.read()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        find_aruco(frame, row)

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def main():
    row = pick_aruco_from_csv('aruco_detection_results.csv')
    open_camera_start_look(row)


if __name__ == '__main__':
    main()
