import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import cv2
import numpy as np
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import random
from http.server import BaseHTTPRequestHandler, HTTPServer


class CaptchaCNN(nn.Module):
    def __init__(self, num_classes=36):
        super(CaptchaCNN, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(128 * 8 * 8, 1024)  # Flattening the convolutional output
        self.fc2 = nn.Linear(1024, 5 * num_classes)  # Output 5 classes for each character

        self.num_classes = num_classes

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)  # Max pooling

        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)

        x = torch.relu(self.conv3(x))
        x = torch.max_pool2d(x, 2)

        x = x.view(x.size(0), -1)  # Flatten

        x = torch.relu(self.fc1(x))
        x = self.fc2(x)

        # Split the output into 5 parts (for 5 characters)
        x = x.view(-1, 5, self.num_classes)

        return x

model = CaptchaCNN(num_classes=36)

if torch.cuda.is_available():
    model.load_state_dict(torch.load("./theModelWeights", weights_only=True))
else:
    model.load_state_dict(torch.load("./theModelWeights", weights_only=True, map_location=torch.device('cpu')))

chars = "123456789abcdefghijklmnopqrstuvwxyz"

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
    transforms.Resize((64, 64)),  # Resize to a fixed size
    transforms.ToTensor(),  # Convert to a tensor
    transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize pixel values
])

if torch.cuda.is_available():
    model = model.to("cuda")

def pred_to_str(prediction):
    predicted_chars = []
    for i in range(5):
        _, predicted = torch.max(prediction[0, i, :], 0)
        predicted_char = str(predicted.item())
        predicted_chars.append(chars[int(predicted_char)-1])
    return ''.join(predicted_chars)

def run_on_image(imagePath):
    with torch.no_grad():
        image = Image.open(imagePath)
        image = transform(image).unsqueeze(0)

        if torch.cuda.is_available():
            image = image.to("cuda")
        outputs = model(image)

        # Get the predicted characters for each position


        captcha_result = pred_to_str(outputs)
        print(f"Predicted CAPTCHA: {captcha_result}")

def runOnImage(image):
    with torch.no_grad():
        image = transform(image).unsqueeze(0)

        if torch.cuda.is_available():
            image = image.to("cuda")
        outputs = model(image)

        # Get the predicted characters for each position


        captcha_result = pred_to_str(outputs)
        print(f"Predicted CAPTCHA: {captcha_result}")
        return captcha_result


from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response, JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
import io
import base64

middleware = [Middleware(CORSMiddleware, allow_origins=['*'])]

async def upload_image(request: Request):
    print(request)

    form = await request.json()
    image_file = form["imageUrl"]  # Expecting multipart file input
    print(image_file)
    
    if not image_file:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)

    image_file = image_file.replace("data:image/png;base64,", "").replace("data:image/jpeg;base64,", "")

    image = Image.open(io.BytesIO(base64.b64decode(image_file)))

    # Pass the image to another function for processing
    processed_image = runOnImage(image)

    return JSONResponse({"result": processed_image})


app = Starlette(middleware=middleware, routes=[
    Route("/post-data", upload_image, methods=["POST"])
])