# KSF 2024: Fixed current logger with RMS calculation
# Uses scan mode for accurate timing and calculates RMS current
from daqhats import mcc118, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string
import time
import csv
from datetime import datetime
import os
import numpy as np

# === Configuration ===
SAMPLE_RATE_HZ = 20000  # 10kHz for accurate AC measurement
SAMPLES_PER_CHANNEL = 100  # Samples per read (10ms window at 10kHz)
PERIOD_SEC = 150  # Save file every n seconds
CH = 4  # Input channel (0-7) - CT connected to CH4
CH_MASK = 1 << CH  # Convert to bit mask (CH4 = 0b00010000 = 16)
SHUNT_OHM = 100.0  # CT shunt resistance
TURNS_RATIO = 1000.0  # CT turns ratio (1000:1)
OUTDIR = os.path.join(".", "Ziresch", "current_data")

# Calculate RMS every N samples (50Hz AC = 20ms period)
# At 10kHz, 200 samples = 20ms = 1 full AC cycle
RMS_WINDOW = 5  # Samples for RMS calculation

os.makedirs(OUTDIR, exist_ok=True)

print("\n========== KSF MCC118 RMS Current Logger ==========")
print(f"Sampling: {SAMPLE_RATE_HZ:,} Hz on CH{CH} (mask: 0x{CH_MASK:02X})")
print(f"RMS Window: {RMS_WINDOW} samples ({RMS_WINDOW/SAMPLE_RATE_HZ*1000:.1f}ms)")
print(f"Save period: {PERIOD_SEC}s")
print(f"Output: {OUTDIR}")
print(f"CT: {TURNS_RATIO:.0f}:1, Shunt: {SHUNT_OHM:g} Ohm\n")

# Initialize HAT
address = select_hat_device(HatIDs.MCC_118)
hat = mcc118(address)
print(f"MCC118 initialized (address: {hat.address()})\n")

# Verify actual sample rate
actual_rate = hat.a_in_scan_actual_rate(1, SAMPLE_RATE_HZ)  # 1 channel
print(f"Requested rate: {SAMPLE_RATE_HZ} Hz")
print(f"Actual rate: {actual_rate} Hz\n")

def get_filename():
    """Generate timestamped filename"""
    now = datetime.now()
    return os.path.join(
        OUTDIR,
        now.strftime("currentdata_%Y-%m-%d_%H-%M-%S.csv")
    )

def voltage_to_current(voltage):
    """Convert CT voltage to primary current"""
    secondary_current = voltage / SHUNT_OHM
    primary_current = secondary_current * TURNS_RATIO
    return primary_current

def calculate_rms(voltages):
    """Calculate RMS current from voltage samples"""
    # Convert to numpy array for fast calculation
    v_array = np.array(voltages)
    # RMS voltage
    v_rms = np.sqrt(np.mean(v_array**2))
    # Convert to primary current
    i_rms = voltage_to_current(v_rms)
    return i_rms

def acquire_with_rms():
    """Acquire data continuously and save RMS values"""
    
    # Start scan
    # Syntax: a_in_scan_start(channel_mask, samples_per_channel, sample_rate_per_channel, options)
    # samples_per_channel: 0 = continuous (no limit on buffer size)
    options = OptionFlags.CONTINUOUS
    samples_per_channel = 0  # 0 = continuous scan
    scan_rate = SAMPLE_RATE_HZ
    
    hat.a_in_scan_start(CH_MASK, samples_per_channel, scan_rate, options)
    print("Scan started. Press Ctrl+C to stop.\n")
    
    # Initialize file
    file = open(get_filename(), "w", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Timestamp", "RMS Current (A)"])
    
    period_start = time.time()
    t0 = time.time()
    voltage_buffer = []
    
    try:
        while True:
            # Read available samples
            read_result = hat.a_in_scan_read(SAMPLES_PER_CHANNEL, -1)
            
            if read_result.hardware_overrun:
                print("\nWARNING: Hardware overrun!")
            if read_result.buffer_overrun:
                print("\nWARNING: Buffer overrun!")
            
            # Add to buffer
            voltage_buffer.extend(read_result.data)
            
            # Calculate RMS when we have enough samples
            while len(voltage_buffer) >= RMS_WINDOW:
                # Take RMS_WINDOW samples
                window = voltage_buffer[:RMS_WINDOW]
                voltage_buffer = voltage_buffer[RMS_WINDOW:]
                
                # Calculate RMS current
                i_rms = calculate_rms(window)

                # Write to file with precise timestamp
                t_rel = time.time() - t0
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                writer.writerow([
                    f"{t_rel:.6f}",
                    timestamp,
                    f"{i_rms:.6f}"
                ])
            
            # Check if period is over
            elapsed = time.time() - period_start
            if elapsed >= PERIOD_SEC:
                file.close()
                samples_written = int(elapsed * SAMPLE_RATE_HZ / RMS_WINDOW)
                print(f"[KSF] Saved ~{samples_written} RMS values. Rotating file...")
                
                # Start new file
                period_start = time.time()
                file = open(get_filename(), "w", newline="", encoding="utf-8")
                writer = csv.writer(file)
                writer.writerow(["Time (s)", "Timestamp", "RMS Current (A)"])
                t0 = period_start
            
            # Small delay to prevent CPU overload
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\n[KSF] Stopped by user.")
    except HatError as error:
        print(f"\nHatError: {error}")
    finally:
        # Stop scan
        hat.a_in_scan_stop()
        hat.a_in_scan_cleanup()
        if not file.closed:
            file.close()
        print("[KSF] Scan stopped. Last file closed.")

if __name__ == "__main__":
    acquire_with_rms()
