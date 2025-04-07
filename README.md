# Pi-BLE-Acessories

Install bleak for BLE on Pi
`sudo pip3 install bleak --break-system-packages`



  <summary>Optional: Make script start in terminal on boot (10 mins)</summary>
  
  
  1. Create the autostart directory if it doesn’t exist:
  ```
  mkdir -p ~/.config/autostart
  ```
  
  2. Create file using nano:
  ```
  nano ~/.config/autostart/start_screen_stream.desktop
  ```
  3. Add the following content, edit the file path if required. Save and exit:
  ```
  [Desktop Entry]
  Type=Application
  Name=Start Screen Stream
  Exec=lxterminal -e "bash -c 'sleep 5; python3 /home/raspberrypi/Desktop/MacPi_Mirror-main/screen_stream.py'"
  X-GNOME-Autostart-enabled=true
  Comment=Delays 5 seconds, then runs screen_stream.py
  ```
  4. Reboot. Terminal will open and run the script after 5 seconds

  

