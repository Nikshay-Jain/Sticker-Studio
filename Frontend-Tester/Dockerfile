FROM python:3.9.6

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Clone the Detectron2 repository from Facebook Research
# This puts the detectron2 directory inside our WORKDIR (/app/detectron2)
RUN git clone https://github.com/facebookresearch/detectron2.git

# Install Detectron2 in editable mode.
RUN pip install --no-cache-dir -e ./detectron2

CMD ["streamlit", "run", "src/app.py"]
