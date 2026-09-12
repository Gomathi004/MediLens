from app.services.ocr_service import extract_text


image_path = "test_medicine.jpg"

try:
    text = extract_text(image_path)

    print("\n--- OCR RESULT ---")
    print(text)

except Exception as e:
    print("\n--- OCR ERROR ---")
    print(e)