import os
import subprocess

def download_file_wget(url, file_path, overwrite=False):
    if os.path.exists(file_path):
        if not overwrite:
            choice = input(f"{file_path} exists. Overwrite? (y/n): ").lower()
            if choice != 'y':
                print(f"Download skipped for {file_path}.")
                return
        print(f"Overwriting {file_path}...")

    print(f"Downloading {url} using wget...")
    subprocess.run(["wget", "-O", file_path, url], check=True)

def select_iso_variant():
    options = ["Cinnamon", "Gnome", "KDE", "LXDE", "LXQt", "Mate", "Standard", "XFCE", "Exit"]
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    choice = int(input("Enter your choice: ")) - 1
    return options[choice].lower() if 0 <= choice < len(options) - 1 else None

def import_gpg_key(key_path):
    subprocess.run(['gpg', '--import', key_path], check=True)

def import_gpg_key_from_keyserver(key_id):
    subprocess.run(["gpg", "--keyserver", "keyserver.ubuntu.com", "--recv-keys", key_id], check=True)

def verify_checksum(checksum_file, file_path, algorithm='sha256'):
    cmd = f"{algorithm}sum -c {checksum_file} 2>/dev/null | grep {file_path} && echo OK || echo Failed"
    subprocess.run(cmd, shell=True, check=True)

def verify_signature(signature_file, checksum_file):
    subprocess.run(['gpg', '--verify', signature_file, checksum_file], check=True)

def main():
    iso_variant = select_iso_variant()
    if not iso_variant:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(script_dir, iso_variant.capitalize())
    os.makedirs(dir_path, exist_ok=True)

    iso_path = os.path.join(dir_path, f"debian-live-12.2.0-amd64-{iso_variant}.iso")

    base_url = "https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid"
    files_to_download = [
        f"debian-live-12.2.0-amd64-{iso_variant}.iso",
        f"debian-live-12.2.0-amd64-{iso_variant}.iso.contents",
        f"debian-live-12.2.0-amd64-{iso_variant}.iso.log",
        f"debian-live-12.2.0-amd64-{iso_variant}.iso.packages",
        "SHA256SUMS",
        "SHA512SUMS",
        "SHA256SUMS.sign",
        "SHA512SUMS.sign",
        "https://ftp-master.debian.org/keys/release-12.asc"
    ]

    for file in files_to_download:
        url = f"{base_url}/{file}" if not file.startswith('http') else file
        file_path = os.path.join(dir_path, os.path.basename(url))
        download_file_wget(url, file_path, overwrite=True)

    key_path = os.path.join(dir_path, "release-12.asc")
    import_gpg_key(key_path)
    import_gpg_key_from_keyserver("DF9B9C49EAA9298432589D76DA87E80D6294BE9B")

    for alg in ['sha256', 'sha512']:
        checksum_file = os.path.join(dir_path, f"{alg.upper()}SUMS")
        signature_file = os.path.join(dir_path, f"{alg.upper()}SUMS.sign")
        verify_checksum(checksum_file, iso_path, alg)
        verify_signature(signature_file, checksum_file)

    print("Debian has been successfully downloaded and verified.")

if __name__ == "__main__":
    main()
