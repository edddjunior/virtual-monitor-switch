# Virtual Monitor Control

A Python app to manage virtual monitors on Linux, using `xrandr` for display control and `xinput` for mouse speed. Features a simple GUI with PyQt5.

## Features

- **Enable Virtual Monitor** (1440x900, scaled to 0.7x0.7)
- **Disable Virtual Monitor**
- **Adjust Mouse Speed**
- **Deskreen Management** (optional)

## Requirements

- Python 3.x
- PyQt5 (`pip install PyQt5`)
- `xrandr`, `xinput`, `ps` (default on most Linux distros)
- **Deskreen** (optional)

## Usage

Run the app:
```bash
python virtual_monitor_control.py
```
It will display buttons to **Enable** or **Disable** the virtual monitor.

## Functions

- `enable_virtual_monitor()`: Activates the virtual monitor and adjusts mouse speed.
- `disable_virtual_monitor()`: Deactivates the virtual monitor.
- `get_mouse_device_name()`: Detects the mouse.
- `adjust_mouse_speed()`: Adjusts mouse speed.
- `check_deskreen_status()`: Checks if Deskreen is running.

## Error Handling

- Notifies if the monitor is already active/inactive.
- Displays errors for `xrandr`/`xinput` issues.
- Warns if the mouse can't be detected.

## GUI

- Title: **Virtual Monitor Control**
- Size: 300x150 px
- Buttons: **Enable Virtual Monitor**, **Disable Virtual Monitor**

## Create Desktop Launcher

1. Create a `.desktop` file:
   ```bash
   nano ~/.local/share/applications/virtual_monitor.desktop
   ```
2. Add this content:
   ```ini
   [Desktop Entry]
   Type=Application
   Name=Virtual Monitor Control
   Exec=python3 /path/to/virtual_monitor_control.py
   Icon=/path/to/icon.png
   Terminal=false
   Categories=Utility;
   ```
3. Save and make executable:
   ```bash
   chmod +x ~/.local/share/applications/virtual_monitor.desktop
   ```

## License

MIT License.

## Author

Developed by edddjunior.

---


#### Very important***
Alongside with this setup, I use Omakube, that relies on Intel Graphics, and as i'm using an Acer Nitro AN515-54, which has NVIDIA controlling its HDMI port, I had to install a property NVIDIA driver to manage only the port and be able to keep the HDMI behaviour while Intel handles the virtual monitors.



### Additional Setup for Tablet as Extra Screen

#### (optional for touch, input and interactive screens) These will work only with Weylus or simmilar solutions

**Enable uinput**:
   ```bash
   sudo groupadd -r uinput
   sudo usermod -aG uinput $USER
   ```

**Firewall**:
   ```bash
   sudo ufw allow 1701/tcp
   sudo ufw allow 9001/tcp
   ```
---

1. **Virtual Displays Setup** (Intel GPU on Xorg):
   ```bash
   sudo apt install xf86-video-intel
   ```

   Create `/etc/X11/xorg.conf.d/20-intel-virtual.conf`:
   ```bash
   Section "Device"
       Identifier "Intel Graphics"
       Driver "intel"
       BusID "PCI:0:2:0"
       Option "VirtualHeads" "2"  # Habilita VIRTUAL1 e VIRTUAL2
   EndSection
   ```
   
   Create `/etc/X11/xorg.conf.d/10-gpu-config.conf`:
   ```bash
   Section "ServerLayout"
       Identifier "layout"
       Screen 0 "intel-screen"
       Option "AllowNVIDIAGPUScreens" "on"
   EndSection
   
   Section "Device"
       Identifier "intel-device"
       Driver "intel"  # Mude de "modesetting" para "intel"
       BusID "PCI:0:2:0"
       Option "VirtualHeads" "1"
   EndSection
   
   Section "Screen"
       Identifier "intel-screen"
       Device "intel-device"
   EndSection
   
   Section "Device"
       Identifier "nvidia-device"
       Driver "nvidia"
       BusID "PCI:1:0:0"
       Option "AllowEmptyInitialConfiguration" "on"
   EndSection
   ```


2. **Configure Virtual Display**:
   ```bash
   gtf 1112 834 60
   xrandr --newmode "1112x834_60.00" 75.81 1112 1168 1288 1464 834 835 838 863 -HSync +Vsync
   xrandr --addmode VIRTUAL1 1112x834_60.00
   xrandr --output VIRTUAL1 --mode 1112x834_60.00
   ```
