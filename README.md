Requirements:
Pyton:
-opencv
-mediapipe
-numpy
xorg-server

To make it work in background create a file_name.service as:

[Unit]
Description=My Volume Control Service
After=network.target

[Service]
ExecStart=/usr/bin/xvfb-run -a -s "-screen 0 640x480x24" /path/to/HandTracking/venv/bin/python3 /path/to/HandTracking/VolumeHandControlAdvanced.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target

then run:
sudo systemctl daemon-reload
sudo systemctl start file_name.service
