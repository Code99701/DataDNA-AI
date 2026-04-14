import cv2

def embed_watermark(image_path, binary_message, output_path):
    img = cv2.imread(image_path)

    data_index = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                if data_index < len(binary_message):
                    img[i][j][k] = (img[i][j][k] & 254) | int(binary_message[data_index])
                    data_index += 1

    cv2.imwrite(output_path, img)
    return output_path