# T440p Libreboot Flashing Guide

## Overview
This guide provides step-by-step instructions to prepare and flash a T440p laptop with Libreboot using a Python script. The script automates several tasks including downloading files, verifying signatures, and preparing the ROM.

## Prerequisites
- A Debian-based GNU/Linux environment.
- Python 3 installed on your system.
- Basic familiarity with terminal commands.

## Installing Python 3
Before running the script, ensure you have Python 3 installed. If not, install it using the following command:
```bash
sudo apt update
sudo apt install python3
```

## Getting Started
1. **Clone the Repository**: If applicable, clone the repository containing the script or download the script directly to your local machine.
   ```
   git clone [URL-to-Repository]
   cd [Repository-Name]
   ```

2. **Script Execution**: Run the script with Python 3.
   ```
   python3 t440p.py
   ```

## Script Workflow
The script follows these steps:

### Step 1: Pre-steps
- Installs necessary packages like `gnupg`, `wget`, and `git`.
- Downloads and imports the Libreboot key (`lbkey.asc`) for signature verification.

### Step 2: Check for `lbmk` Directory
- Ensures the `lbmk` directory exists or clones it from the Git repository.

### Step 3: Download Libreboot Files
- Downloads the latest version of Libreboot and the specific ROM for T440p.

### Step 4: Verify Checksums and Signatures
- Verifies the checksums (`sha256` and `sha512`) and signatures of the downloaded files.

### Step 5: Install Dependencies
- Installs dependencies required for Libreboot and lbmk.

### Step 6: Blob Injection (Optional)
- Asks the user if they wish to inject blobs into the ROM file.

### Step 7: ROM Selection and Preparation
- Lets the user select a ROM file and prepares it for flashing.

### Step 8: Verifying and Preparing for Flashing
- Checks if blobs were correctly inserted.
- Creates necessary `.bin` files and compiles utilities like `nvmutil`.
- Sets a MAC address (random or manual).
- Verifies the integrity of the blob insertion using `hexdump`.
- Makes backups of important files.

### Step 9: Final Preparations
- Prepares the `.rom` file for flashing (internal or external based on user input).

## Flashing the ROM
Once the `.rom` file is prepared, follow the instructions displayed by the script to flash it onto your T440p. This process may vary depending on whether you are performing an internal or external flash.

## Post-Flashing Steps
After successfully flashing the ROM, you may need to:
- Reassemble your laptop if you performed an external flash.
- Set up your BIOS settings according to your preferences.

## Troubleshooting
If you encounter any issues:
- Revisit the steps to ensure all were followed correctly.
- Check for any error messages in the script output and address them accordingly.
- Consult the [Libreboot documentation](https://libreboot.org/docs/) for additional guidance.

## Contributions
Contributions to this script and guide are welcome. Please submit issues or pull requests to the repository.

---

**Note**: Replace `[URL-to-Repository]` and `[Repository-Name]` with the actual URL to your Git repository and its name. Also, ensure that any specific instructions or prerequisites related to your script are accurately reflected in this README.
