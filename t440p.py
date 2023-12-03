import subprocess
import os
import shutil
import stat
import getpass

# Get the base directory relative to the current script
base_dir = os.path.abspath(os.path.dirname(__file__))

# Function to construct paths relative to the base directory
def get_path(*args):
    return os.path.join(base_dir, *args)

# Function to run shell commands
def run_command(command, cwd=None, capture_output=False, use_sudo=False, filename=None):
    cmd = "sudo " + command if use_sudo else command
    try:
        # Check for existing files if filename is provided
        if filename:
            filepath = get_path(cwd, filename) if cwd else get_path(filename)
            if os.path.exists(filepath):
                overwrite = input(f"The file {filename} already exists. Overwrite it? (y/n): ").strip().lower()
                if overwrite == 'n':
                    print(f"Skipping the operation for {filename}")
                    return
        # Execute the command
        result = subprocess.run(cmd, shell=True, check=True, cwd=get_path(cwd) if cwd else None, capture_output=capture_output, text=True)
        if capture_output:
            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        print(f"Error output: {e.stderr}")
        exit(1)

# Clean up the lbmk directory
def clean_up_lbmk_directory(selected_rom, flash_type):
    lbmk_dir = get_path("libreboot/t440p/lbmk")
    modified_rom = f"{selected_rom}.new"
    files_to_keep = [
        "bin", "cbutils", "config", "elf", "projectname", "README.md", "build", "include",
        "script", "src", "tmp", "update", "util", "vendor", "vendorfiles", "version", "versiondate", "mrc", "COPYING", ".git", ".gitignore",
        modified_rom  # Keep the modified ROM file
    ]

    # Add top.rom and bottom.rom to files to keep only if flash type is external
    if flash_type == 'external':
        files_to_keep.extend(["top.rom", "bottom.rom"])

    print("Cleaning up unnecessary files from lbmk directory...")
    for item in os.listdir(lbmk_dir):
        item_path = os.path.join(lbmk_dir, item)
        if item not in files_to_keep:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"Removed file: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item}")

    # Rename the modified .rom file to its original name for consistency
    modified_rom_path = os.path.join(lbmk_dir, modified_rom)
    original_rom_path = os.path.join(lbmk_dir, selected_rom)
    if os.path.exists(modified_rom_path):
        os.rename(modified_rom_path, original_rom_path)
        print(f"Renamed {modified_rom} to {selected_rom}")

    print("Cleanup complete!")
        
# Function to let the user choose a ROM file
def get_rom_choice(directory):
    print("\\nPlease choose a ROM file:")
    rom_files = [f for f in os.listdir(directory) if f.endswith('.rom')]
    for i, rom in enumerate(rom_files):
        print(f"{i + 1}. {rom}")
    while True:
        choice = input("Enter the number corresponding to your choice: ").strip()
        try:
            selected_rom = rom_files[int(choice) - 1]
            return selected_rom
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.\\n")
            
# Function to let the user choose a download mirror
def get_mirror_choice():
    print("\nPlease choose a download mirror based on your location:")
    mirrors = {
        '1': ('https://mirrors.mit.edu/libreboot/', 'MIT, USA'),
        '2': ('https://mirror.math.princeton.edu/pub/libreboot/', 'Princeton University, USA'),
        '3': ('https://mirror.shapovalov.tech/libreboot/', 'Shapovalov.tech, Ukraine'),
        '4': ('https://mirror.koddos.net/libreboot/', 'Koddos.net, Netherlands'),
        '5': ('https://mirror-hk.koddos.net/libreboot/', 'Koddos.net, Hong Kong'),
        '6': ('https://mirror.cyberbits.eu/libreboot/', 'Cyberbits.eu, France'),
        '7': ('https://mirror.mangohost.net/libreboot/', 'Mangohost.net, Moldova')
    }
    
    for key, (url, location) in mirrors.items():
        print(f"{key}. {url} ({location})")
    while True:
        choice = input("Enter the number corresponding to your choice: ").strip()
        if choice in mirrors:
            return mirrors[choice][0]
        else:
            print("Invalid choice. Please try again.\n")

# Main script starts here
if __name__ == "__main__":
    # Step 1: Pre-steps: Download and import lbkey.asc
    print("Step 1: Pre-steps: Download and import lbkey.asc")
    run_command("sudo apt update && sudo apt install -y gnupg wget git")
    run_command("git config --global user.name 'John Doe'")
    run_command("git config --global user.email 'johndoe@example.com'")
    os.makedirs(get_path("libreboot/t440p"), exist_ok=True)
    run_command("wget https://libreboot.org/lbkey.asc -O lbkey.asc", cwd=get_path("libreboot/t440p"), filename="lbkey.asc")    
    run_command("gpg --import {}".format(get_path("libreboot/t440p", "lbkey.asc")))
    
    # Step 2: Check if lbmk directory exists
    print("Step 2: Check if lbmk directory exists")
    lbmk_dir = get_path("libreboot/t440p", "lbmk")
    if not os.path.exists(lbmk_dir):
        print("The lbmk directory does not exist. Cloning from Git repository.")
        run_command("git clone https://codeberg.org/libreboot/lbmk.git", cwd=get_path("libreboot/t440p"))
    else:
        print("The lbmk directory already exists.")
        
    # Step 3: Download latest version of Libreboot and specific ROM for T440p
    print("Step 3: Download the latest version of Libreboot and the specific ROM for T440p")
    selected_mirror = get_mirror_choice()
    base_path = f"{selected_mirror}stable/20230625/"

    # Step 4: Download files from the selected mirror
    print("Step 4: Download files from the selected mirror")
    file_list = [
        "libreboot-20230625_src.tar.xz",
        "libreboot-20230625_src.tar.xz.sha256",
        "libreboot-20230625_src.tar.xz.sha512",
        "libreboot-20230625_src.tar.xz.sig",
        "roms/libreboot-20230625_t440pmrc_12mb.tar.xz",
        "roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sha256",
        "roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sha512",
        "roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sig"
    ]
    for file_name in file_list:
        run_command(f"wget {base_path}{file_name} -O {file_name.split('/')[-1]}", cwd=get_path("libreboot/t440p"), filename=file_name.split('/')[-1])

    # Step 5: Verify the checksums and signatures
    print("Step 5: Verify the checksums and signatures")
    os.chdir(get_path("libreboot/t440p"))
    run_command("sha256sum -c libreboot-20230625_src.tar.xz.sha256")
    run_command("sha512sum -c libreboot-20230625_src.tar.xz.sha512")
    run_command("gpg --verify libreboot-20230625_src.tar.xz.sig libreboot-20230625_src.tar.xz")
    run_command("sha256sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha256")
    run_command("sha512sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha512")
    run_command("gpg --verify libreboot-20230625_t440pmrc_12mb.tar.xz.sig libreboot-20230625_t440pmrc_12mb.tar.xz")
    
    # Step 6: Install lbmk dependencies
    print("Step 6: Install lbmk dependencies")
    lbmk_dir = get_path("libreboot/t440p", "lbmk")

    if not os.path.exists(lbmk_dir):
        print("The lbmk directory does not exist. Please ensure it is properly cloned or created.")
        exit(1)

    os.chdir(lbmk_dir)
    run_command("./build dependencies debian", cwd=lbmk_dir, use_sudo=True)

    # Get the current username
    current_user = getpass.getuser()

    # Correctly set the ownership of the lbmk directory
    run_command(f"chown -R {current_user}:{current_user} {lbmk_dir}", cwd=lbmk_dir, use_sudo=True)

    # Step 7: Ask if the user wants to inject blobs into the ROM .tar.xz file
    print("Step 7: Would you like to inject blobs into the ROM .tar.xz file? "
          "This step is necessary if you haven't already injected blobs into your ROM.")
    user_input = input("Inject blobs? (y/n): ").strip().lower()
    lbmk_path = get_path("libreboot/t440p/lbmk")

    if user_input == 'y':
        print("Injecting blobs into the ROM .tar.xz file...")
        run_command("./vendor inject ../libreboot-20230625_t440pmrc_12mb.tar.xz", cwd=lbmk_path)
    elif user_input == 'n':
        print("Skipping blob injection.")
    else:
        print("Invalid input. Please type 'y' or 'n'. Aborting.")
        exit(1)
    
    # Step 8: Let the user select a ROM file
    print("Step 8: Let the user select a ROM file")
    rom_directory = get_path("libreboot/t440p/lbmk/bin/release/t440pmrc_12mb")
    selected_rom = get_rom_choice(rom_directory)

    # Check if a ROM file was selected
    if selected_rom is not None:
        # Step 9: Copy the selected .rom file
        print(f"Step 9: Copy the selected .rom file: {selected_rom} to the lbmk folder")
        destination_path = get_path("libreboot/t440p/lbmk")  # Ensure get_path function resolves to the correct directory
        shutil.copy(os.path.join(rom_directory, selected_rom), destination_path)
    else:
        # Handle the case where no ROM file was selected
        print("An error occurred: no ROM file was selected. Please try the selection again.")
        exit(1)

    # Step 10: Check that the blobs were inserted
    print("Step 10: Check that the blobs were inserted")
    output = run_command(f"./cbutils/default/cbfstool {selected_rom} print", cwd=get_path("libreboot/t440p/lbmk"), capture_output=True)
    if 'mrc.bin' in output:
        print("mrc.bin found. Proceeding to the next step.")
    else:
        print("mrc.bin not found. Aborting.")
        exit(1)
        
    # Step 11: Create several .bin files to change MAC address and verify integrity of blob insertion
    print("Step 11: Create several .bin files")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}", cwd=get_path("libreboot/t440p/lbmk"))

    # Step 12: Setting a MAC address
    # Compile the nvmutil utility first
    nvmutil_dir = get_path("libreboot/t440p/lbmk/util/nvmutil")
    print(f"Compiling nvmutil in directory: {nvmutil_dir}")
    run_command("make", cwd=nvmutil_dir)

    # Check if nvm binary exists and ensure it is executable
    nvm_path = os.path.join(nvmutil_dir, "nvm")
    if not os.path.isfile(nvm_path):
        print(f"Error: The nvm binary does not exist at {nvm_path}. Please check the make output and ensure that nvmutil is compiled correctly.")
        exit(1)
    os.chmod(nvm_path, os.stat(nvm_path).st_mode | stat.S_IEXEC)

    print("Step 12: Setting a MAC address")
    user_input = input("Set a random MAC address or manually insert one? (random/manual): ").strip().lower()
    if user_input == 'random':
        run_command(f"{nvm_path} flashregion_3_gbe.bin setmac ??:??:??:??:??:??", cwd=get_path("libreboot/t440p/lbmk"))
    elif user_input == 'manual':
        manual_mac = input("Please enter the MAC address in the format XX:XX:XX:XX:XX:XX: ")
        run_command(f"{nvm_path} flashregion_3_gbe.bin setmac {manual_mac}", cwd=get_path("libreboot/t440p/lbmk"))
    else:
        print("Invalid option. Aborting.")
        exit(1)

    # Step 13: Run hexdump to verify the integrity of blob insertion
    print("Step 13: Run hexdump")
    hexdump_output = run_command(f"hexdump -C flashregion_2_intel_me.bin", cwd=get_path("libreboot/t440p/lbmk"), capture_output=True)
    if '0xFF' not in hexdump_output:
        print("No '0xFF' found in hexdump output. The blobs have been inserted correctly.")
    else:
        print("Found '0xFF' in hexdump output. Aborting.")
        exit(1)

    # Step 14: Making a backup of the .rom file
    print("Step 14: Making a backup of the .rom file")
    shutil.copy(get_path("libreboot/t440p/lbmk", selected_rom), get_path("libreboot/t440p/lbmk", f"{selected_rom}.bak"))

    # Step 15: Inserting the modified flashregion_3_gbe.bin
    print("Step 15: Inserting the modified flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -i GbE:flashregion_3_gbe.bin {selected_rom}", cwd=get_path("libreboot/t440p/lbmk"))

    # Step 16: Creating a backup of the modified flashregion_3_gbe.bin
    print("Step 16: Creating a backup of the modified flashregion_3_gbe.bin")
    shutil.copy(get_path("libreboot/t440p/lbmk", "flashregion_3_gbe.bin"), get_path("libreboot/t440p/lbmk", "flashregion_3_gbe.bin.bak"))

    # Step 17: Dumping the new .rom file flashregion_3_gbe.bin
    print("Step 17: Dumping the new .rom file flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}.new", cwd=get_path("libreboot/t440p/lbmk"))

    # Step 18: Comparing the newly dumped flashregion_3_gbe.bin with its backup
    print("Step 18: Comparing the newly dumped flashregion_3_gbe.bin with its backup")
    diff_output = run_command(f"diff flashregion_3_gbe.bin flashregion_3_gbe.bin.bak", cwd=get_path("libreboot/t440p/lbmk"), capture_output=True)
    if diff_output:
        print("Difference found between the files. Please review the differences.")
        exit(1)
    else:
        print("No differences found. The files are identical.")

    # Step 19: Ask if the .rom file is for external or internal flash
    flash_type = input("Are you performing an internal or external flash? (internal/external): ").strip().lower()

    # Validate user input
    if flash_type not in ['internal', 'external']:
        print("Invalid input. Please enter either 'internal' or 'external'.")
        exit(1)

    # Prepare the .rom file for flashing
    if flash_type == 'external':
        print("Preparing the .rom file for external flash.")
        run_command(f"sudo dd if={selected_rom} of=top.rom bs=1M skip=8", cwd=get_path("libreboot/t440p/lbmk"), use_sudo=True)
        run_command(f"sudo dd if={selected_rom} of=bottom.rom bs=1M count=8", cwd=get_path("libreboot/t440p/lbmk"), use_sudo=True)
    else:
        print("The .rom file is ready for internal flash.")
        
    # Step 20: Clean up lbmk directory
    clean_up_lbmk_directory(selected_rom, flash_type)

    print("Congratulations! The .rom file is prepared and ready to be flashed to your T440p. The .rom file you selected is located in 'T440p-Libreboot-Toolkit/libreboot/t440p/lbmk'")
