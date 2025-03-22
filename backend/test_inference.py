from inference import predict_digit

image_path = "test_data.png"

prediction = predict_digit(image_path)
print(f"✅ Predicted Digit: {prediction}")
