#!/usr/bin/env python3

import os
import subprocess
import sys
import shutil

def log(msg):
    print(f"[INFO] {msg}")

def check_command(cmd):
    try:
        subprocess.run([cmd, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def main():
    log("Checking if running on Linux...")
    if not sys.platform.startswith("linux"):
        sys.exit("[ERROR] This script must be run on a Linux system or WSL.")

    log("Creating virtual environment...")

    log("Activating virtual environment and installing dependencies...")
    subprocess.run(["pip", "install", "--upgrade", "pip"])
    subprocess.run(["pip", "install", "prometheus_client"])

    log("Checking for 'iostat' (sysstat)...")
    if not shutil.which("iostat"):
        log("'iostat' not found. Installing sysstat...")
        subprocess.run(["sudo", "apt", "install", "-y", "sysstat"])
    else:
        log("'iostat' is already installed.")

    prometheus_dir = "tracking/prometheus-2.45.0.linux-amd64"
    if not os.path.isdir(prometheus_dir):
        sys.exit(f"[ERROR] Expected directory '{prometheus_dir}' not found. Please place it in the project folder.")

    if not os.path.isfile("tracking/prometheus.yml"):
        sys.exit("[ERROR] prometheus.yml not found in the current directory.")

    log("Moving prometheus.yml into Prometheus directory...")
    shutil.copy("tracking/prometheus.yml", os.path.join(prometheus_dir, "prometheus.yml"))

    log("Starting main Python exporter script...")
    main_proc = subprocess.Popen(["python3", "tracking/main.py"])

    log("Launching Prometheus server...")
    prev_dir = os.getcwd()
    os.chdir(prometheus_dir)
    prometheus_proc = subprocess.Popen(["sudo", "./prometheus", "--config.file=prometheus.yml"])
    os.chdir(prev_dir)

    # Wait for either to finish, or both if needed
    main_proc.wait()
    prometheus_proc.wait()

if __name__ == "__main__":
    main()
