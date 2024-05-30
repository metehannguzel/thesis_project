from ultralytics import YOLO

# Initialize the YOLO model with the given configuration file
model = YOLO("yolov8m.yaml")

# Define hyperparameters for training the model
hparams = {
    "lr0": 0.01,            # Initial learning rate, can be higher than previous value
    "lrf": 0.2,             # Final learning rate factor for the last layers
    "momentum": 0.937,      # Momentum, typically works well around 0.9
    "weight_decay": 0.0005, # Weight decay to help reduce overfitting
    "warmup_epochs": 5,     # Warmup period with a lower initial learning rate
    "warmup_momentum": 0.8, # Momentum during warmup
    "warmup_bias_lr": 0.1,  # Learning rate for biases during warmup
    "box": 0.05,            # Box loss gain, a lower value for faster but potentially less stable learning
    "cls": 0.5,             # Class loss gain, can be left the same
    "dfl": 1.5,             # Distribution focal loss gain for more focus
    "nbs": 64,              # Batch size, can be adjusted based on hardware capabilities
    "hsv_h": 0.015,         # Hue augmentation
    "hsv_s": 0.7,           # Saturation augmentation
    "hsv_v": 0.4,           # Value augmentation
    "degrees": 5.0,         # Random rotation degree
    "translate": 0.1,       # Image translation ratio
    "scale": 0.5,           # Image scaling ratio
    "shear": 0.0,           # Image shearing degree
    "perspective": 0.0,     # Perspective change
    "flipud": 0.0,          # Vertical flip
    "fliplr": 0.5,          # Horizontal flip ratio
}

# Train the model using the specified data and hyperparameters for 32 epochs
results = model.train(data="config_files/config.yaml", epochs=32, **hparams)
