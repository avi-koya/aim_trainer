import cv2
import numpy as np
import csv
import time

# Define video path
video_path = "your_valorant_game.mp4"  # Change this to your file path

# Open the video
cap = cv2.VideoCapture(video_path)

# Define crosshair color range (Adjust based on your crosshair settings)
lower_color = np.array([0, 0, 250])  # Example: Red crosshair (in BGR format)
upper_color = np.array([50, 50, 255])

frame_count = 0
crosshair_positions = []
reaction_times = []
prev_time = time.time()

# Create CSV file to store aim movement
csv_filename = "aim_analysis.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Frame", "X", "Y", "Reaction Time"])  # CSV Headers

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        frame_count += 1
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV for better color filtering
        mask = cv2.inRange(frame, lower_color, upper_color)  # Detect crosshair

        # Find crosshair position
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                crosshair_positions.append((frame_count, cx, cy))

                # Calculate reaction time
                current_time = time.time()
                reaction_time = current_time - prev_time
                prev_time = current_time
                reaction_times.append(reaction_time)
                writer.writerow([frame_count, cx, cy, reaction_time])  # Save to CSV

                # Mark detected crosshair (for debugging)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Display frame (optional)
        cv2.imshow("Valorant Aim Coach", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

print(f"Processed {frame_count} frames. Aim data saved to {csv_filename}.")
