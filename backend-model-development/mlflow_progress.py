import mlflow
import random
import time
import math
import os

# --- Configuration for our Theoretical YOLOv8 Training Run Series ---
EXPERIMENT_NAME = "YOLOv8n-seg_Training_Series_Metrics_comparision"
# RUN_NAME will be generated based on the run number

# --- MAKE SURE THIS LINE IS AT THE TOP OF YOUR SCRIPT ---
NUM_SIMULATED_RUNS = 7 # The number of theoretical models in our series

# Theoretical Training Parameters (Logged once per run) - Can vary slightly per run
THEORETICAL_EPOCHS = 15
THEORETICAL_BATCH_SIZE = 32
THEORETICAL_IMG_SIZE = 640

# Base values for simulating variation across runs
BASE_LR_START = 0.02
LR_END_FACTOR = 0.05

# Base noise levels (can be further tweaked per run simulation if desired)
FAKE_NOISE_LEVEL_LOSS = 0.15
FAKE_NOISE_LEVEL_METRIC = 0.07

# --- Simulate and Log Multiple YOLOv8 Training Runs ---

mlflow.set_experiment(EXPERIMENT_NAME)
print(f"Setting up MLflow Experiment: {EXPERIMENT_NAME}")

print(f"\nInitiating simulation sequence for {NUM_SIMULATED_RUNS} theoretical training runs...")

for run_index in range(NUM_SIMULATED_RUNS):
    # Run number (starting from 1 for naming clarity)
    run_number = run_index + 1
    run_name = f"YOLOv8n_Seg_Run_{run_number:02d}" # e.g., YOLOv8n_Seg_Run_01, _02, etc.

    # Introduce slight variations for each run
    # Use the run index or a random seed based on it to make runs different
    run_seed = 42 + run_index # Vary the random seed for each run
    random.seed(run_seed)

    # Slightly vary theoretical parameters for each run
    theoretical_epochs_this_run = THEORETICAL_EPOCHS # Keep epochs constant for comparison, but you *could* vary this
    theoretical_batch_size_this_run = THEORETICAL_BATCH_SIZE + random.randint(-4, 4) # Vary batch size slightly
    theoretical_img_size_this_run = THEORETICAL_IMG_SIZE # Keep image size constant

    theoretical_lr_start_this_run = BASE_LR_START * (1 + random.uniform(-0.1, 0.1)) # Vary starting LR

    # Vary initial metric/loss bases slightly for each run
    initial_train_loss_base = 2.5 * (1 + random.uniform(-0.1, 0.1))
    initial_val_loss_base = 2.8 * (1 + random.uniform(-0.1, 0.1))
    initial_mAP50B_base = 0.05 * (1 + random.uniform(-0.2, 0.2))
    initial_mAP50_95B_base = 0.02 * (1 + random.uniform(-0.3, 0.3))
    initial_mAP50M_base = 0.03 * (1 + random.uniform(-0.25, 0.25))
    initial_mAP50_95M_base = 0.01 * (1 + random.uniform(-0.4, 0.4))


    # --- Start a NEW MLflow Run for each theoretical model ---
    with mlflow.start_run(run_name=run_name) as run:
        run_id = run.info.run_id
        print(f"\n--- Simulating Run {run_number}/{NUM_SIMULATED_RUNS} (ID: {run_id}) ---")
        print(f"  Simulating {theoretical_epochs_this_run} epochs.")

        # Log parameters for this specific run
        mlflow.log_param("run_number", run_number)
        mlflow.log_param("epochs", theoretical_epochs_this_run)
        mlflow.log_param("batch_size", theoretical_batch_size_this_run)
        mlflow.log_param("img_size", theoretical_img_size_this_run)
        mlflow.log_param("model_type", "yolov8n-seg (Simulated Varied)")
        mlflow.log_param("simulated_dataset", "theoretical_complex_data")
        mlflow.log_param("starting_lr", theoretical_lr_start_this_run)
        mlflow.log_param("simulation_seed", run_seed)

        print("  Theoretical run parameters logged.")

        # --- Simulate Epoch Progress and Log Metrics for THIS run ---
        print("  Simulating epoch-by-epoch training and logging metrics...")

        for epoch in range(theoretical_epochs_this_run):
            current_step = epoch

            # Calculate progress factor (0 to 1) based on THIS run's epochs
            progress = epoch / (theoretical_epochs_this_run - 1) if theoretical_epochs_this_run > 1 else 0

            # --- Simulate Loss Metrics (decreasing with noise) ---
            # Use the run's initial base values and global noise levels
            train_loss_box = initial_train_loss_base * (1 / (1 + 0.1 * epoch)) * (1 + random.uniform(-FAKE_NOISE_LEVEL_LOSS, FAKE_NOISE_LEVEL_LOSS))
            train_loss_cls = initial_train_loss_base * 0.8 * (1 - 0.8 * progress**0.5) * (1 + random.uniform(-FAKE_NOISE_LEVEL_LOSS * 0.8, FAKE_NOISE_LEVEL_LOSS * 0.8))
            train_loss_dfl = initial_train_loss_base * 0.9 * (1 - 0.95 / (1 + math.exp(-0.1 * (epoch - theoretical_epochs_this_run/4)))) * (1 + random.uniform(-FAKE_NOISE_LEVEL_LOSS * 0.9, FAKE_NOISE_LEVEL_LOSS * 0.9))
            train_loss_mask = initial_train_loss_base * 1.2 * (1 - 0.7 * progress**0.7) * (1 + random.uniform(-FAKE_NOISE_LEVEL_LOSS * 1.1, FAKE_NOISE_LEVEL_LOSS * 1.1))

            val_loss_box = train_loss_box * random.uniform(1.0, 1.15)
            val_loss_cls = train_loss_cls * random.uniform(1.0, 1.1)
            val_loss_dfl = train_loss_dfl * random.uniform(1.0, 1.12)
            # CORRECTED LINE: Calculate val_loss_mask based on train_loss_mask
            val_loss_mask = train_loss_mask * random.uniform(1.0, 1.2)

            # Clamp losses to be non-negative
            train_loss_box = max(0.0, train_loss_box)
            train_loss_cls = max(0.0, train_loss_cls)
            train_loss_dfl = max(0.0, train_loss_dfl)
            train_loss_mask = max(0.0, train_loss_mask)
            val_loss_box = max(0.0, val_loss_box)
            val_loss_cls = max(0.0, val_loss_cls)
            val_loss_dfl = max(0.0, val_loss_dfl)
            val_loss_mask = max(0.0, val_loss_mask)


            # --- Simulate Performance Metrics (increasing with noise) ---
            # Use the run's initial base values and global noise levels
            metrics_mAP50_B = initial_mAP50B_base + (0.8 - initial_mAP50B_base) * (1 - math.exp(-0.05 * epoch)) + random.uniform(-FAKE_NOISE_LEVEL_METRIC, FAKE_NOISE_LEVEL_METRIC)
            metrics_mAP50_95_B = initial_mAP50_95B_base + (0.6 - initial_mAP50_95B_base) * (1 - math.exp(-0.03 * epoch)) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 1.2, FAKE_NOISE_LEVEL_METRIC * 1.2)

            metrics_mAP50_M = initial_mAP50M_base + (0.7 - initial_mAP50M_base) * (1 - math.exp(-0.04 * epoch)) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 1.1, FAKE_NOISE_LEVEL_METRIC * 1.1)
            metrics_mAP50_95_M = initial_mAP50_95M_base + (0.5 - initial_mAP50_95M_base) * (1 - math.exp(-0.02 * epoch)) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 1.5, FAKE_NOISE_LEVEL_METRIC * 1.5)

            metrics_precision_B = metrics_mAP50_B * random.uniform(1.0, 1.05) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 0.5, FAKE_NOISE_LEVEL_METRIC * 0.5)
            metrics_recall_B = metrics_mAP50_B * random.uniform(1.0, 1.05) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 0.5, FAKE_NOISE_LEVEL_METRIC * 0.5)
            metrics_precision_M = metrics_mAP50_M * random.uniform(1.0, 1.08) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 0.6, FAKE_NOISE_LEVEL_METRIC * 0.6)
            metrics_recall_M = metrics_mAP50_M * random.uniform(1.0, 1.08) + random.uniform(-FAKE_NOISE_LEVEL_METRIC * 0.6, FAKE_NOISE_LEVEL_METRIC * 0.6)

            # Clamp metrics to plausible ranges (0 to nearly 1)
            metrics_mAP50_B = max(0.0, min(0.995, metrics_mAP50_B))
            metrics_mAP50_95_B = max(0.0, min(0.995, metrics_mAP50_95_B))
            metrics_mAP50_M = max(0.0, min(0.995, metrics_mAP50_M))
            metrics_mAP50_95_M = max(0.0, min(0.995, metrics_mAP50_95_M))
            metrics_precision_B = max(0.0, min(0.995, metrics_precision_B))
            metrics_recall_B = max(0.0, min(0.995, metrics_recall_B))
            metrics_precision_M = max(0.0, min(0.995, metrics_precision_M))
            metrics_recall_M = max(0.0, min(0.995, metrics_recall_M))


            # --- Simulate Learning Rate (decreasing smoothly) ---
            # Cosine decay simulation using THIS run's starting LR
            theoretical_lr_end_this_run = theoretical_lr_start_this_run * LR_END_FACTOR
            lr_pg0 = theoretical_lr_end_this_run + 0.5 * (theoretical_lr_start_this_run - theoretical_lr_end_this_run) * (1 + math.cos(math.pi * progress))
            lr_lrf = theoretical_lr_end_this_run * 0.5 + 0.5 * (theoretical_lr_start_this_run * 0.8 - theoretical_lr_end_this_run * 0.5) * (1 + math.cos(math.pi * progress**1.2))


            # --- Log all the simulated metrics for this epoch ---
            mlflow.log_metrics({
                "train/box_loss": train_loss_box,
                "train/cls_loss": train_loss_cls,
                "train/dfl_loss": train_loss_dfl,
                "train/mask_loss": train_loss_mask,
                "val/box_loss": val_loss_box,
                "val/cls_loss": val_loss_cls,
                "val/dfl_loss": val_loss_dfl,
                "val/mask_loss": val_loss_mask,
                "metrics/precision_B": metrics_precision_B,
                "metrics/recall_B": metrics_recall_B,
                "metrics/mAP50_B": metrics_mAP50_B,
                "metrics/mAP50-95_B": metrics_mAP50_95_B,
                "metrics/precision_M": metrics_precision_M,
                "metrics/recall_M": metrics_recall_M,
                "metrics/mAP50_M": metrics_mAP50_M,
                "metrics/mAP50-95_M": metrics_mAP50_95_M,
                "lr/pg0": lr_pg0,
                "lr/lrf": lr_lrf,
            }, step=current_step)

            # Optional: Add a small delay
            # time.sleep(0.01) # A smaller delay for faster total simulation

        print(f"  Simulated Run {run_number} finished logging {theoretical_epochs_this_run} epochs.")

    # Add a slight pause between runs to make it look like setup time
    time.sleep(0.5)


print(f"\nSimulation of {NUM_SIMULATED_RUNS} training runs complete.")
print("All epoch-level metrics logged for each run.")
print(f"Run 'mlflow ui' in this directory and navigate to the '{EXPERIMENT_NAME}' experiment.")
print("\n--- Instructions for Viewing Multiple Runs on a Single Plot ---")
print("1. In the MLflow UI, click on the experiment name:", EXPERIMENT_NAME)
print(f"2. You will see a table listing your {NUM_SIMULATED_RUNS} runs (e.g., '{run_name.split('_')[0]}_Run_01' through '_07').") # Adjusted name example
print("3. Select the runs you want to compare by clicking the checkbox next to their names.")
print("4. Once runs are selected, go to the 'Metrics' tab on the right.")
print("5. Check the boxes next to the metrics you want to plot (e.g., 'metrics/mAP50-95_M', 'val/box_loss').")
print("MLflow will generate a single plot showing the curves of the selected metric for all selected runs, allowing direct comparison.")
