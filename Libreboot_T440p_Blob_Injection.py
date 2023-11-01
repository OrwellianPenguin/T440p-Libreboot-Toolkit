import subprocess
import os

# Function to run shell commands
def run_command(command, cwd=None, capture_output=False, use_sudo=False):
    cmd = "sudo " + command if use_sudo else command
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, capture_output=capture_output, text=True)
        if capture_output:
            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        print(f"Error output: {e.stderr}")
        exit(1)

# Function to let the user choose a ROM file
def get_rom_choice(directory):
    print("\nPlease choose a ROM file:")
    rom_files = [f for f in os.listdir(directory) if f.endswith('.rom')]
    for i, rom in enumerate(rom_files):
        print(f"{i + 1}. {rom}")
    while True:
        choice = input("Enter the number corresponding to your choice: ").strip()
        try:
            selected_rom = rom_files[int(choice) - 1]
            return selected_rom
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.\n")

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
    run_command("cd /home/user/Documents/Libreboot/T440p && wget https://libreboot.org/lbkey.asc")
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
    run_command(f"cd /home/user/Documents/Libreboot/T440p && wget {base_path}libreboot-20230625_src.tar.xz")
    run_command(f"wget {base_path}libreboot-20230625_src.tar.xz.sha256")
    run_command(f"wget {base_path}libreboot-20230625_src.tar.xz.sha512")
    run_command(f"wget {base_path}libreboot-20230625_src.tar.xz.sig")
    run_command(f"wget {base_path}roms/libreboot-20230625_t440pmrc_12mb.tar.xz")
    run_command(f"wget {base_path}roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sha256")
    run_command(f"wget {base_path}roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sha512")
    run_command(f"wget {base_path}roms/libreboot-20230625_t440pmrc_12mb.tar.xz.sig")

    # Step 5: Verify the checksums and signatures
    print("Step 5: Verify the checksums and signatures")
    run_command("sha256sum -c libreboot-20230625_src.tar.xz.sha256")
    run_command("sha512sum -c libreboot-20230625_src.tar.xz.sha512")
    run_command("gpg --verify libreboot-20230625_src.tar.xz.sig libreboot-20230625_src.tar.xz")
    run_command("sha256sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha256")
    run_command("sha512sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha512")
    run_command("gpg --verify libreboot-20230625_t440pmrc_12mb.tar.xz.sig libreboot-20230625_t440pmrc_12mb.tar.xz")
    
    # Step 6: Install lbmk dependencies
    print("Step 6: Install lbmk dependencies")
    run_command("./build dependencies debian", cwd="/home/user/Documents/Libreboot/T440p/lbmk", use_sudo=True)
    run_command("chown -R user:user lbmk", cwd="/home/user/Documents/Libreboot/T440p/", use_sudo=True)

    # Step 7: Inject blobs into ROM
    print("Step 7: Inject blobs into the ROM .tar.xz file")
    run_command("./vendor inject /home/user/Documents/Libreboot/T440p/libreboot-20230625_t440pmrc_12mb.tar.xz", cwd="/home/user/Documents/Libreboot/T440p/lbmk")

    # Step 8: Extract ROM after blob injection
    print("Step 8: Extract ROM after blob injection")
    run_command("cd /home/user/Documents/Libreboot/T440p && tar -xJvf libreboot-20230625_t440pmrc_12mb.tar.xz && tar -xJvf libreboot-20230625_src.tar.xz")

    # Step 9: Let the user select a ROM file
    print("Step 9: Let the user select a ROM file")
    selected_rom = get_rom_choice("/home/user/Documents/Libreboot/T440p/bin/t440pmrc_12mb/")
    print(f"You have selected {selected_rom}")

    # Step 10: Copy the selected .rom file
    print("Step 10: Copy .rom file")
    run_command(f"cp /home/user/Documents/Libreboot/T440p/bin/t440pmrc_12mb/{selected_rom} /home/user/Documents/Libreboot/T440p/libreboot-20230625_src/")

    # Step 11: Check that the blobs were inserted
    print("Step 11: Check that the blobs were inserted")
    output = run_command(f"./cbutils/default/cbfstool {selected_rom} print", capture_output=True)
    if 'mrc.bin' in output:
        print("mrc.bin found. Proceeding to the next step.")
    else:
        print("mrc.bin not found. Aborting.")
        exit(1)

    # Step 12: Create several .bin files
    print("Step 12: Create several .bin files")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}")

    # Step 13: Setting a MAC address
    print("Step 13: Setting a MAC address")
    user_input = input("Would you like to set a random MAC address or manually insert one? (random/manual): ").strip().lower()
    if user_input == 'random':
        # Add the command to generate a random MAC address
        run_command("./util/nvmutil/nvm flashregion_3_gbe.bin setmac ??:??:??:??:??:??")
    elif user_input == 'manual':
        manual_mac = input("Please enter the MAC address in the format XX:XX:XX:XX:XX:XX: ")
        run_command(f"./util/nvmutil/nvm flashregion_3_gbe.bin setmac {manual_mac}")
    else:
        print("Invalid option. Aborting.")
        exit(1)

    # Step 14: Run hexdump
    print("Step 14: Run hexdump")
    hexdump_output = run_command("hexdump flashregion_2_intel_me.bin", capture_output=True)
    if 'ffff' not in hexdump_output:
        print("No '0xFF' found in hexdump output. Ready to flash the .rom file.")
    else:
        print("Found '0xFF' in hexdump output. Aborting.")
        exit(1)

    # Step 15: Making a backup of the .rom file
    print("Step 15: Making a backup of the .rom file")
    run_command(f"cp {selected_rom}.rom {selected_rom}.rom.bak")

    # Step 16: Inserting the modified flashregion_3_gbe.bin
    print("Step 16: Inserting the modified flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -i GbE:flashregion_3_gbe.bin {selected_rom}.rom")

    # Step 17: Creating a backup of the modified flashregion_3_gbe.bin
    print("Step 17: Creating a backup of the modified flashregion_3_gbe.bin")
    run_command("cp flashregion_3_gbe.bin flashregion_3_gbe.bin.bak")

    # Step 18: Dumping the new .rom file flashregion_3_gbe.bin
    print("Step 18: Dumping the new .rom file flashregion_3_gbe.bin")
    run_command(f"./cbutils/default/ifdtool -x {selected_rom}.rom.new")

    # Step 19: Comparing the newly dumped flashregion_3_gbe.bin with its backup
    print("Step 19: Comparing the newly dumped flashregion_3_gbe.bin with its backup")
    run_command("diff flashregion_3_gbe.bin flashregion_3_gbe.bin.bak")

# End of the script

