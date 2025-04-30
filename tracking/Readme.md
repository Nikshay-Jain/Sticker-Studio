# DA5402 - Assignment 6
## Nikshay Jain | MM21B044

## Overview
This project is a **Prometheus metrics exporter** that collects and exposes system performance metrics, including:

- **Disk I/O Statistics** (Read/Write rates, TPS, Bytes/sec)
- **CPU Utilization** (User, System, Idle, IOWait, etc.)
- **Memory Usage** (Data extracted from `/proc/meminfo`)

The script runs on **Linux** and utilizes the `iostat` command for disk and CPU statistics.

## Features
- Collects real-time **disk I/O, CPU, and memory metrics**
- Exposes metrics via **Prometheus HTTP server** (default **port: 18000**)
- Logs errors and important events to **logs.log**
- **Gracefully exits** after a set duration or when interrupted (`Ctrl+C`) in the terminal.

## Requirements
- **Linux system** - Ubuntu preferred
- Python **3.12+**
- `iostat` (from `sysstat` package)
- Prometheus Client Library

### System set-up
Get the working directory set-up to run the project by:
```bash
git clone https://github.com/Nikshay-Jain/DA5402-Assign-6.git
cd ./DA5402-Assign-6
```

This project can be executed only in `Linux` environment, so `Windows` users can make use of WSL by starting an Ubuntu terminal by:
```bash
wsl -d Ubuntu
```

Setup a virtual environment for this project by:
```bash
python3 -m venv venv
source venv/bin/activate
```
Get prometheus folder installed in the `DA5402-Assign-6` directory for the system to work.

Then, move the `prometheus.yml` inside the prometheus-linux folder by:
```bash
mv prometheus.yml prometheus-2.45.0.linux-amd64/
``` 

### Install Dependencies
Execute the following commands in the terminal 
```bash
sudo apt install sysstat
pip install prometheus_client
```

## Usage (Tasks 1,2,3)
### Run the Python script & activate prometheus
*Note: The script runs for **360 seconds** by default. Modify `run_duration` inside the script to change this.*

```bash
python3 main.py
```

In another Ubuntu terminal, execute:
```bash
cd prometheus-2.45.0.linux-amd64/
sudo ./prometheus --config.file=prometheus.yml
```

### Access Metrics
Once the script is running, you can fetch the metrics for `task 1 & 2` via:
```bash
http://localhost:18000/metrics
```
A sample output from the same can be seen in `18000-metrics.pdf` file.

For `task 3`, prometheus UI can b accessed by
```bash
http://localhost:9090/
```
A sample output from the same can be seen in `9090-graphs.pdf` file.

## Exposed Metrics
### Disk I/O Metrics
| Metric | Description |
|--------|-------------|
| `io_read_rate{device="sda"}` | Disk read rate (transfers/sec) |
| `io_write_rate{device="sda"}` | Disk write rate (transfers/sec) |
| `io_tps{device="sda"}` | Total disk transfers/sec |
| `io_read_bytes{device="sda"}` | Disk read rate in bytes/sec |
| `io_write_bytes{device="sda"}` | Disk write rate in bytes/sec |

### CPU Usage Metrics
| Metric | Description |
|--------|-------------|
| `cpu_avg_percent{mode="user"}` | CPU % in user mode |
| `cpu_avg_percent{mode="system"}` | CPU % in system mode |
| `cpu_avg_percent{mode="idle"}` | CPU % in idle state |
| `cpu_avg_percent{mode="iowait"}` | CPU % waiting for I/O |
| ... |

### Memory Usage Metrics
| Metric | Description |
|--------|-------------|
| `meminfo_memtotal` | Total system memory |
| `meminfo_memfree` | Free system memory |
| `meminfo_buffers` | Memory used for buffers |
| `meminfo_cached` | Cached memory |
| ... |

## Logging
#### Logs are stored in the file named `logs.log`, providing:
- Start/Stop events
- Errors (e.g., `iostat` missing)
- Unexpected metric formats

#### Graceful Shutdown
- **Auto-stops after 360 seconds** (configurable via `run_duration` in main.py)
- Supports **manual exit via Ctrl+C** in the terminal.

## Troubleshooting
### `FileNotFoundError: [Errno 2] No such file or directory: '/proc/meminfo'`
**Solution:** The script is designed for Linux. `/proc/meminfo` is unavailable on Windows.

So, `Linux system` or `WSL` is mandatory for this project. 

### `iostat: command not found`
**Solution:** Install `sysstat`:
```bash
sudo apt install sysstat  # Debian/Ubuntu
sudo yum install sysstat  # RHEL/CentOS
```

## Closing Note
For any other error, the logs can be referred to debug.