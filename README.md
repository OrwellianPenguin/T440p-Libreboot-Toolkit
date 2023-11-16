# T440p Libreboot Flashing Guide

## Overview
This guide provides step-by-step instructions to prepare and flash a T440p laptop with Libreboot using a Python script. The script automates several tasks including downloading files, verifying signatures, and preparing the ROM.

## Prerequisites
- A Debian-based GNU/Linux environment.
- Python 3 and 'git' installed on your system.
- Basic familiarity with terminal commands.
- Update the EC with the stock firmware before flashing Libreboot

You can update from Windows with the BIOS Update Utility or a bootable CD:

https://support.lenovo.com/us/en/downloads/ds037575-bios-update-utility-bootable-cd-for-windows-10-81-8-64-bit-7-32-bit-64-bit-thinkpad-t440p

## Add your user to the sudoers file
To enable sudo permissions for your regular user (not root), follow these steps:
1. **Open Terminal and Become Root** (if not already):
   ```bash
   su
   ```
2. **Edit the sudoers File with visudo**:
   ```bash
   sudo visudo
   ```
![Screenshot from 2023-11-16 01-18-29](https://github.com/OrwellianPenguin/T440p-Libreboot-Toolkit/assets/149578247/72eb13b4-f62b-4799-93fa-2ec2e6461e3d)

3. **Add User Entry**: Below the group sudo entry, add a line for your user: 

   - Format: `username    ALL=(ALL:ALL) ALL`
   - Replace `username` with the your actual username.
4. **Save and Exit**: Press `CTRL+X`, then `CTRL+Y` to save changes.
5. **Test Sudo Access**: Switch to the user account and test sudo access:
   ```bash
   sudo usermod -aG sudo username
   ```

## Installing Git & Python3
Before running the script, ensure you have Python 3 installed. If not, install it using the following command:
```bash
sudo apt update
sudo apt install git && sudo apt install python3
```

## Getting Started
1. **Clone the Repository**: If applicable, clone the repository containing the script or download the script directly to your local machine.
   ```
   git clone https://github.com/OrwellianPenguin/T440p-Libreboot-*
   cd T440p-Libreboot-Toolkit
   ```

2. **Script Execution**: Run the script with Python 3.
   ```
   python3 t440p.py
   ```

## Script Workflow
The script follows these steps:

## Step 1: Pre-steps
- Installs necessary packages like `gnupg`, `wget`, and `git`.
- Downloads and imports the Libreboot key (`lbkey.asc`) for signature verification.

## Step 2: Check for `lbmk` Directory
- Ensures the `lbmk` directory exists or clones it from the Git repository.

## Step 3: Download Libreboot Files
- Downloads the latest version of Libreboot and the specific ROM for T440p.

## Step 4: Verify Checksums and Signatures
- Verifies the checksums (`sha256` and `sha512`) and signatures of the downloaded files.

## Step 5: Install Dependencies
- Installs dependencies required for Libreboot and lbmk.

## Step 6: Blob Injection

- This step is essential for the initial setup to inject necessary blobs into the ROM file.
  When re-running the script, you'll have the option to skip this step if you're using a ROM file that already has the blobs injected.

#### First-Time Users:

- It's crucial to perform blob injection during your first setup. The script will prompt you to inject blobs.

#### Returning Users:

- If you're using a ROM file that was previously prepared with the necessary blobs, you can opt to skip this step. The script will ask if you want to inject blobs again.

## Step 7: ROM Selection and Preparation
- Lets the user select a ROM file and prepares it for flashing.

## Step 8: Verifying and Preparing for Flashing
- Checks if blobs were correctly inserted.
- Creates necessary `.bin` files and compiles utilities like `nvmutil`.
- Sets a MAC address (random or manual).
- Verifies the integrity of the blob insertion using `hexdump`.
- Makes backups of important files.

## Step 9: Final Preparations
- Prepares the `.rom` file for flashing (internal or external based on user input). 
The .rom file is located inside:
```
cd T440p-Libreboot-Toolkit/libreboot/t440p/lbmk
```

## (Optional) Updating the Firmware Internally
If you choose to update the firmware internally, follow these steps:

**Note**: This is only availbile after you flash the firmware externally!

### Install flashrom
To install flashrom, use the following command:
```bash
sudo apt install flashrom
```

### Check Flashing Capability
Before proceeding, verify if your device supports internal flashing:
```bash
sudo flashrom -p internal
```

### Create and Verify Dumps
Run this command to create the firmware dumps and verify them. Ensure the hashes match for safety.
```bash
sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump1_internal.bin && sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump2_internal.bin && sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump3_internal.bin && sha1sum dump1_internal.bin && sha1sum dump2_internal.bin && sha1sum dump3_internal.bin
```
**Important**: Save these dumps to a USB drive for backup.

### Erase and Rewrite Chip Contents
To erase and rewrite the chip contents, use:
```bash
sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -w libreboot.rom
```
**Note**: The `force_I_want_a_brick` option disables safety checks in `flashrom`. It's necessary in some cases but use it cautiously. Ensure you're using the correct ROM for your machine.

### Troubleshooting: /dev/mem Access Error?
If you encounter an error related to /dev/mem access, reboot with the `iomem=relaxed` kernel parameter. Modify GRUB settings by running:
```bash
sudo nano /etc/default/grub
```
![Screenshot from 2023-11-16 01-39-11](https://github.com/OrwellianPenguin/T440p-Libreboot-Toolkit/assets/149578247/e315e2ed-0367-4f72-ba14-04e314f989a7)
Add `iomem=relaxed` to the line:
```
Example: GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iomem=relaxed"
```
Save changes and reboot.

## Other issues?
If you encounter any issues:
- Revisit the steps to ensure all were followed correctly.
- Check for any error messages in the script output and address them accordingly.
- Consult the [Libreboot documentation](https://libreboot.org/docs/) for additional guidance.

## Contributions
Contributions to this script and guide are welcome. Please submit issues or pull requests to the repository.
