import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import json

# Load trained model
try:
    model = tf.keras.models.load_model('asl_model.h5')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Load class indices
try:
    with open('class_indices.json', 'r') as f:
        class_indices = json.load(f)
    # Create a reverse mapping from index to label
    labels = {v: k for k, v in class_indices.items()}
    print("Class indices loaded successfully.")
except Exception as e:
    print(f"Error loading class indices: {e}")
    exit()

# Initialize MediaPipe Hands with improved parameters
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract bounding box with padding
            h, w, c = frame.shape
            cx_min = cy_min = w
            cx_max = cy_max = 0

            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                if cx < cx_min: cx_min = cx
                if cy < cy_min: cy_min = cy
                if cx > cx_max: cx_max = cx
                if cy > cy_max: cy_max = cy

            # Add padding (20% of the bounding box size)
            padding_x = int((cx_max - cx_min) * 0.2)
            padding_y = int((cy_max - cy_min) * 0.2)

            # Ensure the padded coordinates are within the image boundaries
            cx_min = max(0, cx_min - padding_x)
            cy_min = max(0, cy_min - padding_y)
            cx_max = min(w, cx_max + padding_x)
            cy_max = min(h, cy_max + padding_y)

            # Draw bounding box
            cv2.rectangle(frame, (cx_min, cy_min), (cx_max, cy_max), (0, 255, 0), 2)

            # Crop and resize hand region
            hand_img = frame[cy_min:cy_max, cx_min:cx_max]
            if hand_img.size == 0:
                continue

            # Display the cropped hand region in a separate window
            hand_img_resized = cv2.resize(hand_img, (200, 200))
            cv2.imshow('Hand Region', hand_img_resized)

            # Prepare for prediction
            hand_img = cv2.resize(hand_img, (64, 64))
            hand_img = hand_img.astype('float32') / 255.0
            hand_img = np.expand_dims(hand_img, axis=0)

            # Predict
            prediction = model.predict(hand_img)
            confidence = np.max(prediction)
            class_index = np.argmax(prediction)

            # Set a confidence threshold
            if confidence > 0.7:
                predicted_label = labels[class_index]
                color = (0, 255, 0)  # Green for confident predictions
            else:
                predicted_label = "Uncertain"
                color = (0, 0, 255)  # Red for uncertain predictions

            # Display result with confidence
            cv2.putText(frame, f"{predicted_label} ({confidence:.2f})", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Add instructions to the frame
    cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow('Sign Language Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()