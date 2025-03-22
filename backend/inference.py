import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Define the same model architecture used in training
class DigitClassifier(nn.Module):
    def __init__(self):
        super(DigitClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # [batch, 32, 14, 14]
        x = self.pool(torch.relu(self.conv2(x)))  # [batch, 64, 7, 7]
        x = x.view(-1, 64 * 7 * 7)                 # Flatten for FC
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load trained model
model = DigitClassifier()
model.load_state_dict(torch.load('model/mnist_model.pth'))
model.eval()

# Preprocess canvas image like MNIST
def preprocess_image(image):
    image = image.resize((28, 28))
    image = transforms.ToTensor()(image)
    image = image.squeeze()

    # Threshold to binary
    image = (image < 0.5).float()

    # Crop digit bounding box
    rows = torch.any(image, dim=1)
    cols = torch.any(image, dim=0)
    if not torch.any(rows) or not torch.any(cols):
        return torch.zeros((1, 1, 28, 28))  # blank image fallback

    rmin, rmax = torch.where(rows)[0][[0, -1]]
    cmin, cmax = torch.where(cols)[0][[0, -1]]

    image = image[rmin:rmax + 1, cmin:cmax + 1]

    # Resize to 20x20, then pad to 28x28
    image = transforms.Resize((20, 20))(image.unsqueeze(0)).squeeze(0)
    padding = (4, 4, 4, 4)
    image = transforms.Pad(padding)(image)

    # Normalize like MNIST
    image = (image - 0.5) / 0.5
    return image.unsqueeze(0).unsqueeze(0)

# Predict digit from image path
def predict_digit(image_path):
    image = Image.open(image_path).convert("L")
    image = preprocess_image(image)

    # Optional: visualize what the model sees
    # import matplotlib.pyplot as plt
    # plt.imshow(image.squeeze().numpy(), cmap='gray')
    # plt.title("Preprocessed Input")
    # plt.show()

    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()

    return prediction
