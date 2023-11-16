# T440p-Libreboot-Toolkit (Manual Method)

This is important! Please read!

Pre-steps: Download lbkey.asc from https://libreboot.org/download.htmland import it into your keyring. You will need it in order to verify the signature of the files you’re downloading. Make sure you’re downloading the new key not the old one.
Full key fingerprint: 98CC DDF8 E560 47F4 75C0 44BD D0C6 2464 FA8B 4856

To import the lbkey.asc run these commands:

# Install gnupg:

sudo apt update && sudo apt install gnupg

# To confirm that gpg has been installed correctly, you can check its version by running:

gpg --version

# To import the lbkey.asc:

gpg --import lbkey.asc

NOTE: After running gpg --import lbkey.asc, you may see a message saying "1 signature not checked due to a missing key." This is a common occurrence and typically not a cause for concern. This message indicates that the imported key has been signed by another key that you don't have in your keyring. As long as the fingerprint of the key you're importing matches with the trusted source, your key is considered secure and you can proceed.

# Verify the fingerprint of the key to ensure that you've imported the correct one. You can list the keys in your keyring with:

gpg --list-keys

# You should see the key you just imported. To specifically check its fingerprint, you can use:

gpg --fingerprint "98CC DDF8 E560 47F4 75C0 44BD D0C6 2464 FA8B 4856"

========================================================================

I suggest making a folder to put all the files in to keep it neat, for the sake of conveience goto your Documents folder (/home/user/Documents) and make a new folder called ‘Libreboot’. This folder is where we are going to extract the files you’ve downloaded. You can move lbkey.asc into this folder as well if you’d like.

cd /home/user/Documents/Libreboot/T440p

THIS INSTALL GUIDE WAS MADE FOR DEBIAN GNU/LINUX AND RASPBIAN/DIETPI!

Step 1: Go to https://libreboot.org/download.html and scroll down a bit until you find ‘HTTPS mirrors’ to a mirror where you can download the latest version of libreboot (I used https://mirrors.mit.edu/libreboot/ but you can choose any mirror you’d like!) As of writing this (09/25/2023), the latest stable version is ‘libreboot-20230625_src.tar.xz’, download it but don’t extract yet. Make sure you also download the .rom image you need, navigate to /libreboot/stable/20230625/roms/ (it should be right above where you downloaded the src file) and download ‘libreboot-20230625_t440pmrc_12mb.tar.xz’, don’t extract it yet. Download the .sha256, .sha512, and .sig files as well. You will need these in order to verify they haven’t been tampered with. Make sure you move all these downloaded files to your ‘Libreboot’ folder.

# To verify the checksums and signatures run:

sha256sum -c libreboot-20230625_src.tar.xz.sha256 && sha512sum -c libreboot-20230625_src.tar.xz.sha512 && gpg --verify libreboot-20230625_src.tar.xz.sig libreboot-20230625_src.tar.xz && sha256sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha256 && sha512sum -c libreboot-20230625_t440pmrc_12mb.tar.xz.sha512 && gpg --verify libreboot-20230625_t440pmrc_12mb.tar.xz.sig libreboot-20230625_t440pmrc_12mb.tar.xz

# Now that you’ve verified the files, you can safely extract them by running this command in the Libreboot folder:

tar -xJvf libreboot-20230625_src.tar.xz && tar -xJvf libreboot-20230625_t440pmrc_12mb.tar.xz

=========================================================================Step 2: Download and extract lbmk-master.tar.gz

# Run this command to download using wget and extract using tar
wget https://codeberg.org/libreboot/lbmk/archive/master.tar.gz -O lbmk-master.tar.gz && tar -xzvf lbmk-master.tar.gz

sudo chown -R user:user bin lbmk

Optionally, you can also use git to download the file if you prefer to do it that way!

You should make sure to initialize your Git properly, before you begin or else the build system will not work properly. Do this:
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
git clone https://codeberg.org/libreboot/lbmk.git

ATTENTION: The Libreboot folder you created should now have the extracted folders lbmk, libreboot-20230625_src, & a folder named bin (the ‘bin’ folder is the extracted ‘libreboot-20230625_t440pmrc_12mb.tar.xz’ file which contains the .rom files). Remember, the Libreboot folder needs to be in ‘/home/user/Documents/Libreboot/’ to follow this guide without any issues.

=========================================================================
Step 3: From your Libreboot folder, cd into ‘lbmk’, type su (switches to root, make sure you enter root password, not your regular users password), and copy/run this command to build dependencies:

su -c 'cd /home/user/Documents/Libreboot/T440p/lbmk && ./build dependencies debian'

=========================================================================
Step 4: Exit out of the lbmk folder ‘cd ..’and cd into ‘bin’ and cd into the next folder called ‘t440pmrc_12mb’ , this is where the .rom files are (Type ‘ls’ to view all files in folder).
# Run this command below to copy the .rom file of your choice to your ‘libreboot-20230625_src’ folder.
cd /home/user/Documents/Libreboot/T440p/bin/t440pmrc_12mb && cp grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom /home/user/Documents/Libreboot/T440p/libreboot-20230625_src/
========================================================================

STEP 5: BELOW IS REQUIRED, IF YOU DON’T FOLLOW YOU WILL BRICK YOUR BOARD:

PLEASE NOTE: THIS ONLY PATCHES A SINGLE .ROM FILE (RUN THESE AS SUDO)

Step 5a: Inject the blobs:

# Run the following command to inject the necessary blobs into your ROM file:
cd /home/user/Documents/Libreboot/T440p/libreboot-20230625_src/ && ./blobutil inject -r grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom -b t440pmrc_12mb -m 00:f6:f0:40:71:fd

NOTE: The -m flag allows you to set a custom MAC address. Replace 00:f6:f0:40:71:fd with your desired MAC address. You cannot run two Libreboot computers on the same network if they both have the same exact MAC address.

=========================================================================
Step 5b: Check that the blobs were inserted:

./cbutils/default/cbfstool grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom print

Once you see the list of things in there, look for ‘mrc.bin’, if it’s there continue to Step 5c, if its not there, DO NOT CONTINUE THAT MEANS THE BLOBS WEREN’T INJECTED. It should look like this if it was injected correctly:

mrc.bin                        0x78fdc0   mrc            190180 none

=========================================================================
Step 5c: This command below will create several .bin files, one of which says me in it (Intel ME).

./cbutils/default/ifdtool -x grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom

After running the command, the output in terminal should look like this:
File grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom is 12582912 bytes
  Flash Region 0 (Flash Descriptor): 00000000 - 00000fff 
  Flash Region 1 (BIOS): 00021000 - 00bfffff 
  Flash Region 2 (Intel ME): 00003000 - 00020fff 
  Flash Region 3 (GbE): 00001000 - 00002fff 
  Flash Region 4 (Platform Data): 00fff000 - 00000fff (unused)

=========================================================================
Step 5d: Run hexdump on the newly created .bin file to check the output. If it’s all 0xFF (all ones) below or if it is not a bunch of code, then the Intel ME firmware wasn’t inserted. Run this command to run hexdump on the file:

hexdump flashregion_2_intel_me.bin

001a020 ffff ffff ffff 36ff 7fdf 7f7f 7f7f 7f7f
001a030 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f
*
001a060 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f ff60 ffff
001a070 ffff ffff ffff ffff ffff ffff ffff ffff
*
001a500 ffff ffff ffff ffff 7fff fe8c 5e5e d058
001a510 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0
001a520 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c
001a530 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8
001a540 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0
001a550 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c
001a560 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8
001a570 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0
001a580 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c
001a590 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0 d0f8
001a5a0 f80c 0cd0 d0f8 f80c 0cd0 d0f8 f80c 0cd0
001a5b0 d0f8 f80c 0cd0 fff8 ffff ffff ffff ffff
001a5c0 ffff ffff ffff ffff ffff ffff ffff ffff
*
001e000

If you do not see ‘0xFF’ in this entire output, hooray! You’re ready to flash the .rom file!

=========================================================================

Step 6: Use scp on your laptop to copy the lbmk directory, the libreboot-20230625_src folder, and the .rom file onto the Raspberry Pi.

scp -i /root/.ssh/id_rsa_raspberrypi2 -r /home/user/Documents/Libreboot/{lbmk,libreboot-20230625_src/grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom} user@192.168.3.4:/home/user/Documents/

# SSH into Raspberry Pi

sudo ssh -i /root/.ssh/id_rsa_raspberrypi2 user@192.168.3.4

# Create the Libreboot directory, if it does not already exist

mkdir -p /home/user/Documents/Libreboot

# Move the lbmk directory, libreboot-src, and .rom file into the Libreboot directory

mv /home/user/Documents/{lbmk,libreboot-20230625_src,grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom} /home/user/Documents/Libreboot/

# Navigate to the lbmk directory and build dependencies

cd /home/user/Documents/Libreboot/lbmk && sudo ./build dependencies ubuntu2004

=========================================================================
Step 7: Setting up flashrom and enabling spidev on the RaspberryPi

On your RaspberryPi goto terminal and type: ‘sudo raspi-config’ > Select ‘Interface Options’ > Select ‘SPI’ > Enable 

# Make sure flashrom is installed 

sudo apt-get install flashrom

=========================================================================
Step 8: Install pigpio

Flashrom on the RPi may not be able to detect the SPI flash chip on some systems, even if your wiring and clip are set up perfectly. This may be due to the drive strength of the Raspberry Pi GPIOs, which is 8mA by default. Drive strength is essentially the maximum current the pin can output while also maintaining the minimum high-level voltage. In the case of the Pi, this voltage is 3.0V.
Fortunately, the drive strength of the Raspberry Pi can be increased up to 16mA. There are a few tools that can set this, such as the pigs utility from the pigpio project. On the Raspberry Pi OS, the following commands should install pigpio and set the drive strength to 16mA:
# Install pigpio:
sudo apt install pigpio
# Start the pigpiod daemon, which the pigs utility communicates with to interact with the gpios:
sudo pigpiod
# Set the drive strength of GPIO group 0, which contains the spi0 pins, to 16mA:
pigs pads 0 16 
# You can check the current drive strength using
pigs padg 0
WARNING: If the chipset is very strongly trying to drive a pin to a value opposite that of the Pi, more than 16mA pass through the Pi’s GPIO pins, which may damage them as they are only designed for 16mA. The drive strength is NOT a current limit. That said, this is a risk to the Pi regardless of the drive strength. Resistors between the chipset and the flash should protect against this, though not all boards have these.
=========================================================================
# Change directory to the Libreboot folder, create a backup of the .rom file, and split the .rom into two files (bottom.rom and top.rom). Copy and run the entire command below:
cd /home/user/Documents/Libreboot/T440p/ && cp grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom.backup && sudo dd if=grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom bs=1M of=bottom.rom count=8 && sudo dd if=grub_t440pmrc_12mb_libgfxinit_corebootfb_usqwerty.rom bs=1M of=top.rom skip=8
=========================================================================
[THE COMMAND BELOW IS OPTIONAL, NOT REQUIRED FOR THIS GUIDE!]
NOTE: For boards with more than one flash chip, you will need to read from both chips and combine them into a single file. Most of the time, a two-chip setup includes one 8MB 'bottom' chip and one 4MB 'top' chip. The setup just described applies to the x230, t430, t530, and t440p. For other boards, make sure you know which chip contains the lower and upper portions of the ROM. You can combine both flashes together with 'cat', for example:
cat bottom.rom top.rom > full_12mb.rom
NOTE: You will only need this combined ROM if you intend to manually extract blobs. For this guide, you don't need to do that.
# Shut down your RaspberryPi to prepare for flashing
sudo shutdown now
=========================================================================
Step 10: Prepare your Raspberry Pi!

WARNING: DO NOT ATTACH/DETACH THE CLIP WHEN THE RASPBERRYPI IS ON! **PRESS THE KILLSWITCH BUTTON TO ENSURE THERE IS NO POWER DRAWING!**

NOTE: Pin 3 and 7 on the SOIC 8 clip are not used. Also, make sure you cordinate Pin 1 on the SOIC 8 clip to the dot on the BIOS chip.
After you powered down the RaspberryPi and attached the clip to the top (4MB) chip, you can turn it back on. Make sure you cd into your Libreboot folder ‘cd /home/user/Documents/Libreboot’ and run the command below on the RaspberryPi:
# Check to see if flashrom is working
cd /home/user/Documents/Libreboot && sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768
NOTE: On some systems, higher speeds will be unstable. On those systems, try lower speed like spispeed=4096 or even spispeed=2048 which should, in most cases, work just fine but it will obviously be slower. The spispeed=32768 setting works just fine on most setups if you use short wires, within 10cm.
=========================================================================


Step 11: Create dump files, create a backup of the dumps, and flash the top chip
# Run this command to create the top chip dumps and verify their hashes (Make sure the hashes match)
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -r dump1_top.bin && sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -r dump2_top.bin && sha1sum dump1_top.bin && sha1sum dump2_top.bin
If the checksums match, it indicates that you have a good dump. If they do not, check your wiring. Wires should be within 10cm length for best stability, and they should all be the same length (VCC and GND wires can be longer).
ATTENTION: BACK UP THE DUMP FILES TO TWO USB DRIVES!
You can now write the .rom file for the top chip! Proceed:
# Run this command to flash the top chip
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -w /home/user/Documents/Libreboot/top.rom
Once that command outputs the following, the flash has completed successfully. If not, just flash again.
Reading old flash chip contents... done.
Erasing and writing flash chip... Erase/write done.
Verifying flash... VERIFIED.
Again, use a lower spispeed value if you need to, for stability.
Make sure to turn off the RaspberryPi before detaching the chip and clipping it to the bottom chip.
# Shutdown your RaspberryPi and attach the clip to the bottom chip
sudo shutdown now
=========================================================================
Step 12: Create dump files, create a backup of the dumps, and flash the bottom chip (Flip the clip to match the dot on the BIOS chip)
# Run the command to create the bottom chip dumps and verify its hashes
cd /home/user/Documents/Libreboot/ && sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 && sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -r dump1_bottom.bin && sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -r dump2_bottom.bin && sha1sum dump1_bottom.bin && sha1sum dump2_bottom.bin

ATTENTION: BACK UP THE DUMP FILES TO TWO USB DRIVES!
You can now write to the bottom chip! Proceed:
# Run this command to flash the bottom chip
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=32768 -w /home/user/Documents/Libreboot/bottom.rom
Reading old flash chip contents... done.
Erasing and writing flash chip... Erase/write done.
Verifying flash... VERIFIED.
Turn off the RaspberryPi before detaching the clip to reassemble your new Libreboot laptop!
Welcome to the free world!
=========================================================================
Updating the firmware internally:
Run flashrom on host CPU
You can simply take any ROM image from the libreboot project, and flash it. Boot a Linux distribution on the target device, and install flashrom.
In some cases, this is not possible or there are other considerations. Please read this section carefully.
# Check to see if you can flash internally
sudo flashrom -p internal
# Run this command to create the dumps and verify them (Make sure the hashes match)
cd /home/user/Documents/Libreboot/T440p/ && sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump1_internal.bin && sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump2_internal.bin && sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -r dump3_internal.bin && sha1sum dump1_internal.bin && sha1sum dump2_internal.bin && sha1sum dump3_internal.bin
MAKE SURE TO SAVE THESE TO TWO SEPERATE USB DRIVES!
How to erase and rewrite the chip contents:
sudo flashrom -p internal:laptop=force_I_want_a_brick,boardmismatch=force -w libreboot.rom
If you are re-flashing a GM45+ICH9M laptop (e.g. ThinkPad X200/X200S/X200T, T400, T500, R400, W500 etc - but not R500), you should run the ich9gen utility to preserve your mac address. Please read the ich9utils documentation: /docs/install/ich9utils.html
NOTE: force_I_want_a_brick is not scary. Do not be scared! This merely disables the safety checks in flashrom. Flashrom and coreboot change a lot, over the years, and sometimes it’s necessary to use this option. If you’re scared, then just follow the above instructions, but remove that option. So, just use -p internal. If that doesn’t work, next try -p internal:boardmismatch=force. If that doesn’t work, try -p internal:boardmismatch=force,laptop=force_I_want_a_brick. So long as you ensure you’re using the correct ROM for your machine, it will be safe to run flashrom. These extra options just disable the safetyl checks in flashrom. There is nothing to worry about.
If successful, it will either say VERIFIED or it will say that the chip contents are identical to the requested image.
=========================================================================
NOTE: There are exceptions where the above is not possible. Read about them in the sections below:
If running flashrom -p internal for software/internal based flashing, and you get an error related to /dev/mem access, you should reboot with iomem=relaxed kernel parameter before running flashrom, or use a kernel that has CONFIG_STRICT_DEVMEM not enabled.
To fix the /dev/mem error run the command below:
sudo nano /etc/default/grub
Add ‘iomem=relaxed’ to the end of this line:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iomem=relaxed"
Save changes, reboot, and try running flashrom internally again!
sudo shutdown now
