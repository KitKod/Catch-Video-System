# Catch-Video-System

###### 1. Завантаження та встановлення драйвера для кулеру:
	1) cd ~/Downloads/
	2) git clone https://github.com/Pyrestone/jetson-fan-ctl.git
	3) cd jetson-fan-ctl/
	4) sudo ./install.sh
	
###### 2. Налаштування встроєного драйверу для роботи з SD card та відеокамерою IMX477
URL: https://wiki.seeedstudio.com/J101_Enable_SD_Card/:

	1) cd ~/Downloads/
	2) git clone https://github.com/Seeed-Studio/seeed-linux-dtoverlays.git
	3) cd seeed-linux-dtoverlays
	4) sed -i '17s#JETSON_COMPATIBLE#\"nvidia,p3449-0000-b00+p3448-0002-b00\"\, \"nvidia\,jetson-nano\"\, \"nvidia\,tegra210\"#' overlays/jetsonnano/jetson-sdmmc-overlay.dts
	5) make overlays/jetsonnano/jetson-sdmmc-overlay.dtbo
	6) sudo cp overlays/jetsonnano/jetson-sdmmc-overlay.dtbo /boot/
	7) Перевірка камери на роботу з консолі
	
	Якщо камеру під'єднано до першого роз'єму:
	DISPLAY=:0.0 gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)20/1' ! nvoverlaysink -e
	Якщо камеру під'єднано до другого роз'єму:
	DISPLAY=:0.0 gst-launch-1.0 nvarguscamerasrc sensor-id=1 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)20/1' ! nvoverlaysink -e
	
	Якщо камери працюють, то виконати наступну команду та перейти на підпункт 9):
	DEPRECATED: sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc"
        sudo /opt/nvidia/jetson-io/config-by-hardware.py -n "reComputer sdmmc"
	
	8) Виконати наступну команду у випадку, коли камера не працює з консолі:
	sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX477 Dual"
	
	Також є можливість налаштувати драйвер на камери IMX219 або на Camera IMX477-A та IMX219-B одночасно, якщо вони під'єднані до різних роз'ємів, наступними командами:
	sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX219 Dual"
	або
	sudo /opt/nvidia/jetson-io/config-by-hardware.py -n 1="reComputer sdmmc" 2="Camera IMX477-A and IMX219-B"
	
	9) sudo reboot now
	
###### 3. Копіювання системи на SD card для подальшої роботи з неї, оскільки 16 ГБ встроєної пам'яті не вистачає для встановлення потрібних компонентів.

URL: https://www.forecr.io/blogs/bsp-development/change-root-file-system-to-sd-card-directly:

	1) lsblk
	Перевірити чи примонтована SD card  (mmcblk1 або mmcblk1p1)
	2) Зробити umount для SD card, якщо вона примонтована (Команда залежить від місця куди примонтована карта)
	sudo umount точка_монтажу
	NEW FLOW:
		3) sudo jetson_clocks
		4) gnome-disks
		5) Format the whole SD disk before creating the storage. IMPORTANT: use GPT
		6) Create partition in EXT4
		7) Check new name of device: should look like /dev/mmcblk1p1
		COPY the root system to SD
		8) Download script to copy system: https://github.com/mistelektronik/forecr_blog_files/raw/master/change_rootfs_storage_direct-emmc_to_sdmmc.zip
		9) Run the script: sudo ./change_rootfs_storage_direct-emmc_to_sdmmc.sh {DEVICE_NAME_OF_EXTERNAL_STORAGE}
			Example: sudo ./change_rootfs_storage_direct-emmc_to_sdmmc.sh /dev/mmcblk1p1
		10) sudo reboot now
		11) Use it to check result: df -h

	DEPRECATED:
		3) sudo mkfs.ext4 /dev/mmcblk1
		4) sudo nano /boot/extlinux/extlinux.conf
		Знайти строчки APPEND та замінити mmcblk0p1 на mmcblk1 (Їх дві)
		Зберегти файл
		5) sudo mount /dev/mmcblk1 /mnt
		6) sudo cp -ax / /mnt
		7) sudo umount /mnt/
		8) sudo reboot now
	
###### 4. Завантаження системи з SD card та встановлення необхідних компонентів:
	1) sudo apt update
	2) sudo apt upgrade
	3) sudo apt install nvidia-jetpack

###### 5. Завантаження SCI Camera та тестування:
	1) cd ~/Downloads/ 
	2) git clone https://github.com/JetsonHacksNano/CSI-Camera.git
	3) cd CSI-Camera
	4) Перевірка скриптів

###### 6. Setup python and libs:
	1) Install GTK models: sudo apt-get install libcanberra-gtk-module libcanberra-gtk3-module
	2) Install python 3.8:  `sudo apt install python3.8`
	3) Install venv and pip: `sudo apt install python3.8-venv & sudo apt-get install python3.8-dev`
	4) Switch to use python 3.8: ```sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 & sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 & sudo update-alternatives --config python3```
	5) Install PIP: `sudo apt install python3-pip`
	6) Install the lib (OR use requirements.txt): pip install nanocamera 

###### 7. Build OpenCV from sources
We need it to be able use cv2 in python3.8:

1. Install Required Dependencies:
```
sudo apt update
sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3.8-dev python3.8-venv \
    libtbb2 libtbb-dev libdc1394-22-dev libeigen3-dev
```

2. Download OpenCV and OpenCV Contrib Sources:
```
mkdir ~/opencv_build
cd ~/opencv_build
git clone -b 4.1.1 https://github.com/opencv/opencv.git
git clone -b 4.1.1 https://github.com/opencv/opencv_contrib.git
```

3. Create and Activate a Python Virtual Environment (Optional but Recommended):
```
python3.8 -m venv opencv_env
source opencv_env/bin/activate
```

4. Configure the Build with CMake:

```
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
```
make -j$(nproc)
```

6. Install OpenCV:
```
sudo make install
sudo ldconfig
```

7. Verify the Installation:
```
python3.8
import cv2
print(cv2.__file__)
print(cv2.__version__)
```

###### 8. Check that cameras works

```
python3.8 ./sandbox/usb_camera_simple_test_v1.py
```







