# Sticker-Studio
## Nikshay Jain | MM21B044
## Sahil Kokare | MM21B036

## Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
   - [Module 1: Data Partitioning](#module-1-orchestration)
   - [Module 2: Model Training](#frontend-testing)
5. [Closing Note](#closing-note)

---

## Project Overview
Want to develop get a sticker? Go ahead.

This project focuses on training & evaluating finetuned YOLO-v8n models for image segmentation and sticker generation. The project is divided into modules including data scraping, partitioning, model training, hyperparameter tuning, performance evaluation and application development.

---

## Directory Structure

```bash
project_root/
├── Backend-Model-Development/   # Orchestration module
├── Frontend-Tester/             # Code to test model and use app
└── Readme.md                    # Project documentation
```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nikshay-Jain/Sticker-Studio.git
   cd Sticker-Studio
   ```

2. **Install Dependencies**:
   WSL (Ubuntu) preferrably or Mac.
   Ensure you have Python 3.9 installed to the required libraries:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   pip install -r requirements.txt
   ```
   This file installs the libraries used by the code:
    - piexif
    - streamlit
    - tensorflow
    - stability-sdk
    - scikit-learn
    - pillow
    - pycocotools
    - fvcore
    - cython
    - opencv-python
    - cython
    - mlflow
    - prometheus_client

3. **Set Up detectron2**:
   
   ```bash
   python3 Frontend-Tester/src/install_detectron2.py
   ```
---

## Usage
![alt text](image.png)
### Module 1: Orchestration:
The Scraper module is set to run daily via a custom cronjob.

### Module 2: Frontend & Testing:

```bash
cd Frontend-Tester
streamlit run src/app.py
```
The workflow is explained in the block diagram above.
Dockerfile is attached to make this app platform independent.

---

## Closing Note:
In case of debugging, the log files can be referred in the `logs/` folder.

### Credits:
Nikshay Jain | MM21B044
Sahil Kokare | MM21B036