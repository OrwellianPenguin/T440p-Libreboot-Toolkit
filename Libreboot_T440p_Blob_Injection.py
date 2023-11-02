import subprocess
import os
import shutil
import stat

# Function to run shell commands
def run_command(command, cwd=None, capture_output=False, use_sudo=False, filename=None):
    cmd = "sudo " + command if use_sudo else command
    try:
        # Check for existing files if filename is provided
        if filename:
            filepath = os.path.join(cwd, filename)
            if os.path.exists(filepath):
                overwrite = input(f"The file {filename} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
                if overwrite == 'no':
                    print(f"Skipping download of {filename}")
                    return
        
        # Execute the command
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, capture_output=capture_output, text=True)
        if capture_output:
            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        print(f"Error output: {e.stderr}")
        exit(1)

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
    run_command("mkdir -p /home/user/Documents/Libreboot/T440p")
    run_command("wget https://libreboot.org/lbkey.asc -O lbkey.asc", cwd="/home/user/Documents/Libreboot/T440p", filename="lbkey.asc")    
    run_command("gpg --import /home/user/Documents/Libreboot/T440p/lbkey.asc")
    
    # Step 2: Check if lbmk directory exists
    print("Step 2: Check if lbmk directory exists")
    lbmk_dir = "/home/user/Documents/Libreboot/T440p/lbmk"
    if not os.path.exists(lbmk_dir):
        print("The lbmk directory does not exist. Cloning from Git repository.")
        run_command("git clone https://codeberg.org/libreboot/lbmk.git", cwd="/home/user/Documents/Libreboot/T440p")
    else:
        print("The lbmk directory already exists.")
    
    # Step 3: Download latest version of Libreboot and specific ROM for T440p
    print("Step 3: Download latest version of Libreboot and specific ROM for T440p")
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
    cwd_path = "/home/user/Documents/Libreboot/T440p"
    for file_name in file_list:
        run_command(f"wget {base_path}{file_name} -O {file_name.split('/')[-1]}", cwd=cwd_path, filename=file_name.split('/')[-1])

    # Step 5: Verify the checksums and signatures
    print("Step 5: Verify the checksums and signatures")
    run_command("sha256sum -c libreboot-20230625_src.tar.xz.sha256", cwd=cwd_path)
    run_command("sha512sum -c libreboot-20230625_src.tar.xz.sha512", cwd=cwd_path)
    run_command("gpg --verify libreboot-20230625_src.tar.xz.sig libreboot-20230625_src.tar.xz", cwd=cwd_path)
    run_command("sha256sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha256", cwd=cwd_path)
    run_command("sha512sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha512", cwd=cwd_path)
    run_command("gpg --verify libreboot-20230625_t440pmrc_12mb.tar.xz.sig libreboot-20230625_t440pmrc_12mb.tar.xz", cwd=cwd_path)

    # Step 6: Install lbmk dependencies
    print("Step 6: Install lbmk dependencies")
    run_command("./build dependencies debian", cwd="/home/user/Documents/Libreboot/T440p/lbmk", use_sudo=True)
    run_command("chown -R user:user lbmk", cwd="/home/user/Documents/Libreboot/T440p/", use_sudo=True)
    
    # Step 7: Ask if user wants to inject blobs into the ROM .tar.xz file
    print("Step 7: Would you like to inject blobs into the ROM .tar.xz file? This step is necessary if you haven't already injected blobs into your ROM.")
    user_input = input("Inject blobs? (yes/no): ").strip().lower()

    if user_input == 'yes':
        print("Injecting blobs into the ROM .tar.xz file...")
        run_command("./vendor inject /home/user/Documents/Libreboot/T440p/libreboot-20230625_t440pmrc_12mb.tar.xz", cwd="/home/user/Documents/Libreboot/T440p/lbmk")
    elif user_input == 'no':
        print("Skipping blob injection.")
    else:
        print("Invalid input. Please type 'yes' or 'no'. Aborting.")
        exit(1)

    # Step 8: Let the user select a ROM file
    print("Step 8: Let the user select a ROM file")
    selected_rom = get_rom_choice("/home/user/Documents/Libreboot/T440p/lbmk/bin/release/t440pmrc_12mb")
    print(f"You have selected {selected_rom}")

    # Step 9: Copy the selected .rom file
    print("Copying selected .rom file to lbmk folder...")
    run_command(f"cp /home/user/Documents/Libreboot/T440p/lbmk/bin/release/t440pmrc_12mb/{selected_rom} /home/user/Documents/Libreboot/T440p/lbmk", cwd="/home/user/Documents/Libreboot/T440p/lbmk/bin/release/t440pmrc_12mb")

    # Step 10: Check that the blobs were inserted
    print("Step 10: Check that the blobs were inserted")
    output = run_command(f"./cbutils/default/cbfstool {selected_rom} print", cwd="/home/user/Documents/Libreboot/T440p/lbmk", capture_output=True)
    if 'mrc.bin' in output:
        print("mrc.bin found. Proceeding to the next step.")
    else:
        print("mrc.bin not found. Aborting.")
        exit(1)

    # Step 11: Create several .bin files to change MAC address and verify integrity of blob insertion
    print("Step 11: Create several .bin files")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 12: Setting a MAC address
    # Compile the nvmutil utility first
    nvmutil_dir = "/home/user/Documents/Libreboot/T440p/lbmk/util/nvmutil"
    print(f"Compiling nvmutil in directory: {nvmutil_dir}")
    print(f"Current working directory before make: {os.getcwd()}")
    make_output = run_command("make", cwd=nvmutil_dir)
    print("Make output:", make_output)

    # Check if nvm binary exists
    nvm_path = os.path.join(nvmutil_dir, "nvm")
    if not os.path.isfile(nvm_path):
        print(f"Error: The nvm binary does not exist at {nvm_path}. Please check the make output and ensure that nvmutil is compiled correctly.")
        exit(1)

    # Ensure the binary is executable
    os.chmod(nvm_path, os.stat(nvm_path).st_mode | stat.S_IEXEC)

    print("Step 12: Setting a MAC address")
    user_input = input("Would you like to set a random MAC address or manually insert one? (random/manual): ").strip().lower()
    if user_input == 'random':
        # Command to set a random MAC address using the ?? placeholder for random bytes
        run_command(f"{nvm_path} flashregion_3_gbe.bin setmac ??:??:??:??:??:??", cwd="/home/user/Documents/Libreboot/T440p/lbmk")
    elif user_input == 'manual':
        # Prompt the user for a manual MAC address
        manual_mac = input("Please enter the MAC address in the format XX:XX:XX:XX:XX:XX: ")
        # Command to set the MAC address manually
        run_command(f"{nvm_path} flashregion_3_gbe.bin setmac {manual_mac}", cwd="/home/user/Documents/Libreboot/T440p/lbmk")
    else:
        print("Invalid option. Aborting.")
        exit(1)

    # Step 13: Run hexdump
    print("Step 13: Run hexdump")
    hexdump_output = run_command(f"hexdump flashregion_2_intel_me.bin", cwd="/home/user/Documents/Libreboot/T440p/lbmk", capture_output=True)
    if '0xFF' not in hexdump_output:
        print("No '0xFF' found in hexdump output. The blobs have been inserted correctly.")
    else:
        print("Found '0xFF' in hexdump output. Aborting.")
        exit(1)

    # Step 14: Making a backup of the .rom file
    print("Step 14: Making a backup of the .rom file")
    run_command(f"cp {selected_rom} {selected_rom}.bak", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 15: Inserting the modified flashregion_3_gbe.bin
    print("Step 15: Inserting the modified flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -i GbE:flashregion_3_gbe.bin {selected_rom}", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 16: Creating a backup of the modified flashregion_3_gbe.bin
    print("Step 16: Creating a backup of the modified flashregion_3_gbe.bin")
    run_command(f"cp flashregion_3_gbe.bin flashregion_3_gbe.bin.bak", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 17: Dumping the new .rom file flashregion_3_gbe.bin
    print("Step 17: Dumping the new .rom file flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}.new", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 18: Comparing the newly dumped flashregion_3_gbe.bin with its backup
    print("Step 18: Comparing the newly dumped flashregion_3_gbe.bin with its backup")
    run_command(f"diff flashregion_3_gbe.bin flashregion_3_gbe.bin.bak", cwd="/home/user/Documents/Libreboot/T440p/lbmk")
    
    # Step 19: Ask if the .rom file is for external or internal flash
    flash_type = input("Are you performing an internal or external flash? External option splits the .rom into top.rom and bottom.rom. Internal option leaves the .rom unsplit. This will NOT flash your system. (internal/external): ").strip().lower()

    # Validate user input
    if flash_type not in ['internal', 'external']:
        print("Invalid input. Please enter either 'internal' or 'external'.")
        exit(1)

    # Command for both internal and external flash
    common_command = f"mv {selected_rom}.new {selected_rom} && cp {selected_rom} {selected_rom}.bak"

    # If external flash
    if flash_type == 'external':
        external_command = f"sudo dd if={selected_rom} bs=1M of=bottom.rom count=8 && sudo dd if={selected_rom} bs=1M of=top.rom skip=8"
        full_command = f"{common_command} && {external_command}"
    # If internal flash
    else:
        full_command = common_command

    # Execute the appropriate command
    run_command(full_command, cwd="/home/user/Documents/Libreboot/T440p/lbmk", use_sudo=True)

    # The .rom file is ready to be flashed
    print("Congratulations! You're now ready to flash the .rom file(s) to your T440p!")

    # End of the script
