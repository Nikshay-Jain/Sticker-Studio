#!/usr/bin/env python3

import time, logging, subprocess, signal, sys
from prometheus_client import start_http_server, Gauge, CollectorRegistry

# Configure logging for better monitoring and debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tracking/logs.log"),  # Log output to a file
        logging.StreamHandler()  # Display logs in the console
    ]
)

# Use a custom Prometheus registry to avoid collecting default metrics
registry = CollectorRegistry()

# --- Disk I/O and CPU Usage Metrics ---
io_read_rate = Gauge('io_read_rate', 'Disk read rate in transfers per second', ['device'], registry=registry)
io_write_rate = Gauge('io_write_rate', 'Disk write rate in transfers per second', ['device'], registry=registry)
io_tps = Gauge('io_tps', 'Total disk transfers per second', ['device'], registry=registry)
io_read_bytes = Gauge('io_read_bytes', 'Disk read rate in bytes per second', ['device'], registry=registry)
io_write_bytes = Gauge('io_write_bytes', 'Disk write rate in bytes per second', ['device'], registry=registry)
cpu_avg_percent = Gauge('cpu_avg_percent', 'CPU utilization percentage', ['mode'], registry=registry)

def collect_iostat_metrics():
    """
    Collects disk I/O and CPU statistics using the 'iostat' command and updates Prometheus metrics.
    """
    try:
        process = subprocess.run(['iostat'], capture_output=True, text=True, check=True)
        output = process.stdout.strip().split('\n')

        device_stats_started = False
        cpu_stats_started = False
        for line in output:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Device"):
                device_stats_started = True
                continue

            if device_stats_started and line[0].isalpha():
                parts = line.split()
                if len(parts) >= 7:
                    device = parts[0]
                    tps = float(parts[1])
                    read_rate = float(parts[2])
                    write_rate = float(parts[3])
                    read_bytes_per_sec_kb = float(parts[4])
                    write_bytes_per_sec_kb = float(parts[5])

                    io_read_rate.labels(device=device).set(read_rate)
                    io_write_rate.labels(device=device).set(write_rate)
                    io_tps.labels(device=device).set(tps)
                    io_read_bytes.labels(device=device).set(read_bytes_per_sec_kb * 1024)
                    io_write_bytes.labels(device=device).set(write_bytes_per_sec_kb * 1024)

            if line.startswith("avg-cpu") or "CPU" in line:
                cpu_stats_started = True
                continue

            if cpu_stats_started and len(line.split()) >= 5:
                parts = line.split()
                
                if parts[0] == "%user":
                    continue  
                try:
                    cpu_avg_percent.labels(mode='user').set(float(parts[0]))
                    cpu_avg_percent.labels(mode='nice').set(float(parts[1]))
                    cpu_avg_percent.labels(mode='system').set(float(parts[2]))
                    cpu_avg_percent.labels(mode='iowait').set(float(parts[3]))
                    cpu_avg_percent.labels(mode='steal').set(float(parts[4]))
                    cpu_avg_percent.labels(mode='idle').set(float(parts[5]))
                except ValueError:
                    logging.warning(f"Unexpected format in CPU statistics: {line}")
                cpu_stats_started = False  

    except FileNotFoundError:
        logging.error("The 'iostat' command is missing. Ensure it is installed and available.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute 'iostat': {e}")
    except Exception as e:
        logging.error(f"Unexpected error while collecting I/O statistics: {e}")

# --- Memory Usage Metrics ---
meminfo_metrics = {}

def collect_meminfo_metrics():
    """
    Reads memory usage data from '/proc/meminfo' and exposes it as Prometheus metrics.
    Handles cases where the file is unavailable, such as on non-Linux systems.
    """
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo_data = f.readlines()

        for line in meminfo_data:
            line = line.strip()
            if not line:
                continue

            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip().replace('(', '').replace(')', '')
                value_unit = parts[1].strip().split()
                value = int(value_unit[0])
                metric_name = f"meminfo_{key.lower().replace(' ', '_')}"

                if metric_name not in meminfo_metrics:
                    meminfo_metrics[metric_name] = Gauge(metric_name, f'Memory information from /proc/meminfo: {key}', registry=registry)
                
                meminfo_metrics[metric_name].set(value)

    except FileNotFoundError:
        logging.warning("The file '/proc/meminfo' is not available. This is expected on non-Linux systems.")
    except Exception as e:
        logging.error(f"Unexpected error while collecting memory metrics: {e}")

# Handle graceful exit
def graceful_exit(signum, frame):
    logging.info("Termination signal received. Exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)     # Handle Ctrl+C
signal.signal(signal.SIGTERM, graceful_exit)    # Handle kill signal

if __name__ == '__main__':
    start_http_server(18000, registry=registry)
    logging.info("Prometheus metrics server is running on port 18000")

    run_duration = 3600            # Change this to how long you want the script to run (in seconds)
    start_time = time.time()

    while time.time() - start_time < run_duration:
        collect_iostat_metrics()
        collect_meminfo_metrics()
        time.sleep(1)

    logging.info("Metrics collection completed. Exiting.")