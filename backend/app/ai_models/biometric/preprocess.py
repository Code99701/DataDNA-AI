import cv2
import numpy as np
import torch

def preprocess_image(image_path):
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        raise ValueError("Invalid image path")

    # Resize to fixed size
    img = cv2.resize(img, (224, 224))

    # Normalize
    img = img / 255.0

    # Convert to 3 channels (ResNet expects 3)
    img = np.stack([img, img, img], axis=0)

    # Convert to tensor
    img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0)

    return img_tensor