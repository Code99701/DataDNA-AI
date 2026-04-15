import torch
import torchvision.models as models
import torch.nn as nn

# Load pretrained model
model = models.resnet18(pretrained=True)

# Remove classification layer → we only need features
model.fc = nn.Identity()

# Set to evaluation mode
model.eval()

def get_fingerprint_embedding(img_tensor):
    with torch.no_grad():
        embedding = model(img_tensor)
    
    return embedding.numpy()