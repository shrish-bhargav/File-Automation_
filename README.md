# File-Automation_
A script that helps to automate your files ... 

## For Arch-btw systems
### Step 1
clone the repository using `git@github.com:shrish-bhargav/File-Automation_.git`

### Step 2
`cd File-Automation`

### Step 3
`python3 main.py`

## For Nix-Based Systems

Follow steps 1 and 2 and then write `nix-shell` inside your terminal

Then proceed with step 3. 


## TO MAKE SURE THAT THIS RUNS ON THE START OF YOUR SYSTEM (USING SYSTEMCTL)

### Steps:

Create the systemd Service File:

### Steps for Creating the systemd Service:

a. Create a systemd Service File
Navigate to `/etc/systemd/system/` and create a new .service file, for example, file_automation.service:


`sudo nano /etc/systemd/system/file_automation.service`
Add the following content to the file:
```
[Unit]
Description=File Automation Script
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/nix-shell /path/to/your/shell.nix --run "python3 /path/to/your/main.py >> file_automation_log.txt 2>&1" ## for nix-users 
Restart=always
User=your-username
Environment=HOME=/home/your-username
WorkingDirectory=/home/your-username/Documents/code/file_automation
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```
Replace /path/to/your/shell.nix and /path/to/your/main.py with the actual paths to your shell.nix and main.py. Make sure your-username is replaced with your actual username.

b. Reload systemd and Enable the Service:
After saving the file, you need to reload the systemd configuration and enable the service so it starts automatically on boot:

`sudo systemctl daemon-reload`
`sudo systemctl enable file_automation.service`
`sudo systemctl start file_automation.service`
This will:

Reload the systemd manager.
Enable the service to start at boot.
Start the service immediately.
Verify the Service is Running:

To ensure that the service is running correctly, check its status with:

`sudo systemctl status file_automation.service`


Check Logs:

You can view the logs of the service using journalctl:

bash
Copy code
journalctl -u file_automation.service -f
 OR
 you can check file_automation_log.txt 
