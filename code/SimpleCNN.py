import torch
import torch.nn as nn

class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        
        # Convolutional blocks
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.relu3 = nn.ReLU()
        
        # Global average pooling
        self.global_avg_pooling = nn.AdaptiveAvgPool2d(1)
        
        # Fully connected layer
        self.fc = nn.Linear(256, 1)  # Output layer for binary classification

        # Sigmoid activation for binary classification
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Input: (batch_size, 3, 224, 224)
        
        # Convolutional blocks
        x = self.relu1(self.conv1(x))
        x = self.relu2(self.conv2(x))
        x = self.relu3(self.conv3(x))
        
        # Global average pooling
        x = self.global_avg_pooling(x)
        
        # Flatten before fully connected layer
        x = x.view(-1, 256)
        
        # Fully connected layer
        x = self.fc(x)
        
        # Apply sigmoid activation for binary classification
        x = self.sigmoid(x)
        
        return x



    




