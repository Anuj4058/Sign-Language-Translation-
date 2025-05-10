import cv2
import numpy as np
from tensorflow.keras.models import load_model
import string


model = load_model("asl_model.h5")

# A-Z without 'J'
classes = list(string.ascii_uppercase)
classes.remove('J')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    x1, y1, x2, y2 = 100, 100, 300, 300
    roi = frame[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28))
    normalized = resized / 255.0
    reshaped = normalized.reshape(1, 28, 28, 1)

    pred = model.predict(reshaped)
    predicted_index = np.argmax(pred)
    predicted_letter = classes[predicted_index]

    cv2.putText(frame, f'Prediction: {predicted_letter}', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
