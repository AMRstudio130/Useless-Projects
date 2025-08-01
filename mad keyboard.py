import cv2
import random
import time
import numpy as np

# Open the default camera (use CAP_DSHOW on Windows to avoid MSMF warnings)
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a full-screen window
cv2.namedWindow('Bald Stimulator', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Bald Stimulator', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

# Timing and state
start_time = time.time()
duration = 5  # seconds
frozen = False
final_hair_count = 0
final_beard_count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to read from camera.")
        break

    current_time = time.time()
    elapsed = current_time - start_time

    # Resize camera to fit smaller area
    cam_small = cv2.resize(frame, (640, 480))

    # Generate values or freeze them
    if not frozen:
        hair_count = random.randint(150000, 400000)
        beard_count = random.randint(50000, 100000)
        if elapsed >= duration:
            final_hair_count = hair_count
            final_beard_count = beard_count
            frozen = True
    else:
        hair_count = final_hair_count
        beard_count = final_beard_count

    # Create a black canvas for full-screen UI
    canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Add silly heading
    cv2.putText(canvas, '💥 Bald Stimulator 3000 🤯', (60, 60),
                cv2.FONT_HERSHEY_COMPLEX, 1.5, (180, 100, 255), 3, cv2.LINE_AA)

    # Draw camera feed centered
    cam_x = (1280 - cam_small.shape[1]) // 2
    cam_y = 120
    canvas[cam_y:cam_y + 480, cam_x:cam_x + 640] = cam_small

    # Overlay Beard Count
    cv2.putText(canvas, f'🧔 Beard Count: {beard_count:,}', (100, 640),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 100), 3, cv2.LINE_AA)

    # Overlay Hair Count
    cv2.putText(canvas, f'💇 Hair Count: {hair_count:,}', (100, 690),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)

    # Countdown or final message
    if not frozen:
        countdown = max(0, int(duration - elapsed))
        cv2.putText(canvas, f'🔒 Locking in: {countdown}s', (900, 680),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(canvas, '✅ Counts Finalized!', (900, 680),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 255), 2, cv2.LINE_AA)

    # Show on screen and write to file
    cv2.imshow('Bald Stimulator', canvas)
    out.write(cam_small)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s') and frozen:
        cv2.imwrite('final_result.png', canvas)
        print("Snapshot saved as final_result.png")

# Cleanup
cam.release()
out.release()
cv2.destroyAllWindows()


