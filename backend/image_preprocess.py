def preprocess_image(image_path):
    import cv2, os

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Light denoise only
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    base, _ = os.path.splitext(image_path)
    out_path = base + "_clean.png"
    cv2.imwrite(out_path, denoised)

    return out_path