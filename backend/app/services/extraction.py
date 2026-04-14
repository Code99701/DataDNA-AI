def extract_watermark(image_path):
    import cv2

    img = cv2.imread(image_path)
    binary_data = ""
    message = ""

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_data += str(img[i][j][k] & 1)

                # Process every 8 bits
                if len(binary_data) % 8 == 0:
                    char = chr(int(binary_data[-8:], 2))
                    message += char

                    # STOP EARLY
                    if message.endswith("###"):
                        return message.replace("###", "")

    return message