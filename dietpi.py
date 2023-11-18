import subprocess
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Error output: {e.stderr}")
        return None

def verify_checksum(download_path, image_file):
    print("Starting checksum verification...")
    checksum_file = f"{image_file}.sha256"
    os.chdir(download_path)  # Change to download directory
    result = run_command(f"sha256sum -c {checksum_file}")
    if result is None:
        print("Checksum verification failed: Command error")
        return False
    print(f"Checksum verification result: {result}")
    is_valid = "OK" in result
    print(f"Checksum valid: {is_valid}")
    return is_valid

def verify_signature(download_path, image_file):
    print("Verifying the signature...")
    signature_file = f"{image_file}.asc"
    os.chdir(download_path)  # Change to download directory

    try:
        result = subprocess.run(f"gpg --verify {signature_file} {image_file}", shell=True, text=True, capture_output=True)
        print("Output:", result.stdout)  # Print the standard output for debugging
        print("Error Output:", result.stderr)  # Print the error output for debugging
        return "Good signature" in result.stdout or "Good signature" in result.stderr
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during signature verification: {e}")
        return False

def download_file(download_path, url):
    os.makedirs(download_path, exist_ok=True)
    file_name = url.split("/")[-1]
    file_path = os.path.join(download_path, file_name)
    
    # Check if the file already exists
    if os.path.isfile(file_path):
        overwrite = input(f"The file '{file_path}' already exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != 'yes':
            print(f"Download aborted for {file_path}.")
            return True  # Return True to indicate no error, just user choice

    result = run_command(f"wget -q -O {file_path} {url}")
    if result is None:
        print(f"Failed to download {url}")
        return False
    return True

def decompress_image(download_path, image_file):
    print("Decompressing the DietPi image...")
    decompressed_file = image_file.rstrip(".xz")
    decompressed_path = os.path.join(download_path, decompressed_file)

    # Check if the decompressed file already exists
    if os.path.isfile(decompressed_path):
        overwrite = input(f"The decompressed file '{decompressed_path}' already exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != 'yes':
            print("Decompression aborted.")
            return True
        else:
            # Remove the existing file before decompression
            os.remove(decompressed_path)

    result = run_command(f"xz -dk {os.path.join(download_path, image_file)}")
    if result is None:
        print("Failed to decompress the image.")
        return False
    else:
        print("Image decompressed successfully.")
        return True

def install_dietpi():
    print("Starting the DietPi installation process.")

    # Determine the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_directory, 'dietpi')
    
    download_url = "https://dietpi.com/downloads/images/DietPi_RPi-ARMv8-Bookworm.img.xz"
    image_file = download_url.split("/")[-1]

    if not download_file(download_path, download_url) or not download_file(download_path, download_url + ".sha256") or not download_file(download_path, download_url + ".asc"):
        return

    if not verify_checksum(download_path, image_file):
        print("Checksum verification failed.")
        return

    if not verify_signature(download_path, image_file):
        print("Signature verification failed.")
        return

    if not decompress_image(download_path, image_file):
        print("Failed to decompress the image.")
        return

    print("DietPi has been successfully downloaded, verified, and decompressed.")

if __name__ == "__main__":
    install_dietpi()
