# My Volume Control

## Requirements

### Python Packages:
- **opencv**
- **mediapipe**
- **numpy**

### System Dependencies:
- **xorg-server**

## Running in the Background

To run the My Volume Control service in the background, follow these steps:

### Step 1: Create a systemd service file

Create a service file, e.g., `my_volume_control.service`, with the following content:

```ini
[Unit]
Description=My Volume Control Service
After=network.target

[Service]
ExecStart=/usr/bin/xvfb-run -a -s "-screen 0 640x480x24" /path/to/Hand

