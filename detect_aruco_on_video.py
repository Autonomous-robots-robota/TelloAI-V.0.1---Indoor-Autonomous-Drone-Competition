import cv2
import numpy as np
import json
import csv

# Load the video
cap = cv2.VideoCapture('challengeB.mp4')

# Load the predefined dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

# Initialize the detector parameters using default values
parameters = cv2.aruco.DetectorParameters()

# Camera calibration parameters (example values, replace with your actual calibration results)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.array([0.1, -0.25, 0.001, 0.0005, 0.1], dtype=np.float32)

# Define the real-world coordinates of the ArUco marker corners
marker_length = 1.0  # Length of a marker's side
# Output CSV file
csv_filename = 'aruco_detection_results.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame ID', 'QR ID', 'QR 2D', 'QR 3D: dist', 'QR 3D: yaw', 'QR 3D: pitch', 'QR 3D: roll'])

results = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the grayscale image
    corners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If markers are detected, process them
    if markerIds is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)

        for i in range(len(markerIds)):
            # Get the 2D corner points
            corners_2d = corners[i].reshape(4, 2).tolist()

            # Calculate distance to the camera
            distance = np.linalg.norm(tvecs[i])

            # Calculate yaw angle with respect to the camera "lookAt" point
            rmat, _ = cv2.Rodrigues(rvecs[i])
            camera_pos = -np.matrix(rmat).T * np.matrix(tvecs[i]).T
            yaw = np.arctan2(camera_pos[0][0], camera_pos[2][0]) * 180 / np.pi

            # result = {
            #     'frame': int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
            #     'id': markerIds[i],
            #     'corners_2d': corners_2d,
            #     'distance': float(distance),
            #     'yaw': yaw
            # }
            # results.append(result)

            rmat_inv = np.linalg.inv(rmat)
            angles_rad = cv2.RQDecomp3x3(rmat_inv)[0]  # Output in radians
            angles_deg = np.degrees(angles_rad)  # Convert to degrees

            result_row = [
                int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
                markerIds[i][0],
                corners_2d,
                float(distance),
                angles_deg[0],  # yaw
                angles_deg[1],  # pitch
                angles_deg[2]  # roll
            ]
            csv_writer.writerow(result_row)

        # Draw all detected markers and their axes on the frame
        cv2.aruco.drawDetectedMarkers(frame, corners, markerIds)
        for i in range(len(markerIds)):
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)

    # Display the resulting frame
    cv2.imshow('ArUco Marker Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Save the results to a JSON file
with open('aruco_detection_results.json', 'w') as f:
    json.dump(results, f, indent=4)
