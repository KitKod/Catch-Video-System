
# Catch-Video-System

This repository contains instructions for setting up a video capture system using NVIDIA Jetson, cooling fans, SD card, IMX477 camera, and other necessary components. The steps include installing drivers, setting up the SD card, and configuring cameras. Follow the steps below to complete the setup.

## 1. Install Fan Driver

To install the necessary driver for the cooling fan:

1. Navigate to your Downloads directory:
   ```bash
   cd ~/Downloads/
   ```
2. Clone the fan control repository:
   ```bash
   git clone https://github.com/Pyrestone/jetson-fan-ctl.git
   ```
3. Change to the cloned directory:
   ```bash
   cd jetson-fan-ctl/
   ```
4. Run the installation script:
   ```bash
   sudo ./install.sh
   ```

## 2. Configure Built-in Driver for SD Card and IMX477 Camera

For setting up the SD card and IMX477 camera, follow these steps:

1. Navigate to your Downloads directory:
   ```bash
   cd ~/Downloads/
   ```
2. Clone the Seeed Studio overlays repository:
   ```bash
   git clone https://github.com/Seeed-Studio/seeed-linux-dtoverlays.git
   ```
3. Change to the cloned directory:
   ```bash
   cd seeed-linux-dtoverlays
   ```
4. Modify the driver file:
   ```bash
   sed -i '17s#JETSON_COMPATIBLE#"nvidia,p3449-0000-b00+p3448-0002-b00"\, "nvidia\,jetson-nano"\, "nvidia\,tegra210"#' overlays/jetsonnano/jetson-sdmmc-overlay.dts
   ```
5. Compile the overlay:
   ```bash
   make overlays/jetsonnano/jetson-sdmmc-overlay.dtbo
   ```
6. Copy the compiled overlay to the boot directory:
   ```bash
   sudo cp overlays/jetsonnano/jetson-sdmmc-overlay.dtbo /boot/
   ```


### Camera Check

7. To verify camera functionality, use the following command based on the camera port:

   - **First port:**
     ```bash
     DISPLAY=:0.0 gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)20/1' ! nvoverlaysink -e
     ```
   - **Second port:**
     ```bash
     DISPLAY=:0.0 gst-launch-1.0 nvarguscamerasrc sensor-id=1 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)20/1' ! nvoverlaysink -e
     ```

8. If the camera does not work, configure the hardware using the following command:
   ```bash
   sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX477 Dual"
   ```

   - **For IMX219 cameras or mixed IMX477-A and IMX219-B configurations:**
     ```bash
     sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX219 Dual"
     ```
     ```bash
     sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX477-A and IMX219-B"
     ```

9. Reboot the system:
   ```bash
   sudo reboot now
   ```

## 3. Copy the System to SD Card

Given the limited 16GB of internal storage, the system must be copied to an SD card:

1. Verify the SD card is mounted:
   ```bash
   lsblk
   ```
2. If mounted, unmount the SD card:
   ```bash
   sudo umount <mount_point>
   ```

3. Run the following commands to prepare the SD card:
   ```bash
   sudo jetson_clocks
   gnome-disks
   ```
4. Format the SD card using GPT and create an EXT4 partition.
5. Identify the device name (e.g., `/dev/mmcblk1p1`).
6. Download and run the system copy script:
   ```bash
   wget https://github.com/mistelektronik/forecr_blog_files/raw/master/change_rootfs_storage_direct-emmc_to_sdmmc.zip
   unzip change_rootfs_storage_direct-emmc_to_sdmmc.zip
   sudo ./change_rootfs_storage_direct-emmc_to_sdmmc.sh /dev/mmcblk1p1 <or insert here your device name from step above>
   ```
7. Reboot the system:
   ```bash
   sudo reboot now
   ```
8. Verify the result using:
   ```bash
   df -h
   ```

## 4. Install Necessary Components

1. Update the package list and upgrade installed packages:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
2. Install NVIDIA JetPack:
   ```bash
   sudo apt install nvidia-jetpack
   ```


## 5. Install and Test SCI Camerav (you can skip this step if you use USB)

1. Navigate to your Downloads directory:
   ```bash
   cd ~/Downloads/
   ```
2. Clone the CSI Camera repository:
   ```bash
   git clone https://github.com/JetsonHacksNano/CSI-Camera.git
   ```
3. Change to the CSI-Camera directory:
   ```bash
   cd CSI-Camera
   ```
4. Test the scripts as needed.

## 6. Setup Python and Libraries

1. Install GTK modules:
   ```bash
   sudo apt-get install libcanberra-gtk-module libcanberra-gtk3-module
   ```
2. Install Python 3.8:
   ```bash
   sudo apt install python3.8
   ```
3. Install `venv` and `pip`:
   ```bash
   sudo apt install python3.8-venv
   sudo apt-get install python3.8-dev
   ```
4. Switch to Python 3.8 (we need this vesrion for OpenCV. Please replace <python3.6> to your current version on JETSON):
   ```bash
   sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
   sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
   sudo update-alternatives --config python3
   ```
5. Install PIP:
   ```bash
   sudo apt install python3-pip
   ```
6. Install the required libraries:
   ```bash
   pip install nanocamera
   ```

## 7. Build OpenCV from Source

We need it to be able use cv2 in python3.8:

### Prerequisites

1. Install required dependencies:
   ```bash
   sudo apt update
   sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
       libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
       libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
       gfortran openexr libatlas-base-dev python3.8-dev python3.8-venv \
       libtbb2 libtbb-dev libdc1394-22-dev libeigen3-dev
   ```

### Download and Build OpenCV

2. Download OpenCV and OpenCV Contrib sources:
   ```bash
   mkdir ~/opencv_build
   cd ~/opencv_build
   git clone -b 4.1.1 https://github.com/opencv/opencv.git
   git clone -b 4.1.1 https://github.com/opencv/opencv_contrib.git
   ```
3. Create and activate a Python virtual environment:
   ```bash
   python3.8 -m venv opencv_env
   source opencv_env/bin/activate
   ```
4. Configure the build with CMake:
   ```bash
   cmake -D CMAKE_BUILD_TYPE=Release \
         -D CMAKE_INSTALL_PREFIX=/usr/local \
         -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
         -D PYTHON3_EXECUTABLE=$(which python3.8) \
         -D PYTHON3_INCLUDE_DIR=$(python3.8 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
         -D PYTHON3_PACKAGES_PATH=$(python3.8 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
         -D WITH_CUDA=ON \
         -D CUDA_ARCH_BIN=5.3 \
         -D CUDA_ARCH_PTX="" \
         -D ENABLE_FAST_MATH=ON \
         -D CUDA_FAST_MATH=ON \
         -D WITH_CUBLAS=ON \
         -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 ..
   ```
5. Build OpenCV:
   ```bash
   make -j$(nproc)
   ```
6. Install OpenCV:
   ```bash
   sudo make install
   sudo ldconfig
   ```

7. Verify the installation:
   ```bash
   python3.8
   ```

   ```
   # insert into python CLI

   import cv2
   print(cv2.__file__)
   print(cv2.__version__)
   ```

8. Check that code of the Project can use the CSI/USB cameras
   ```bash
   python3.8 ./sandbox/usb_camera_simple_test_v1.py
   ```
   If script above raises `ModuleNotFoundError: No module named 'cv2'` error, add following lines at the top of the script
   ```
   import sys
   sys.path.append('/usr/lib/python3.8/site-packages')
   print(sys.path
   ```

9. TODO: Install PyTourh with CUDA support
