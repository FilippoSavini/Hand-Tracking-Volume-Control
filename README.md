# Volume Control
To control the volume with hand gestures via a webcam.
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
ExecStart=/usr/bin/xvfb-run -a -s "-screen 0 640x480x24" /path/to/HandTracking/venv/bin/python3 /path/to/HandTracking/VolumeHandControlAdvanced.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

### Step 2: Reload systemd and Start the Service

Run the following commands to reload systemd and start the service:

```ini
sudo systemctl daemon-reload
sudo systemctl start my_volume_control.service
```

Now, your My Volume Control service should be up and running in the background.

Note: Replace /path/to/HandTracking with the actual path to your HandTracking directory.








