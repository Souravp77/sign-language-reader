import cv2

# Start webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit the webcam window.")

while True:
    ret, frame = cap.read()
    cv2.imshow('Webcam Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()