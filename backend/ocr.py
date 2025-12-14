def extract_text(image_path: str) -> str:
    """
    Runs OCR on a preprocessed image and returns raw text.
    """

    import cv2      # lazy imports
    import pytesseract

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    text = pytesseract.image_to_string(
        img,
        config="--oem 3 --psm 6"
    )

    return text