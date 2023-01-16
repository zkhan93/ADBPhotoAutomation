# Android Night Picture Automator

This repository contains code that uses ADB to automate clicking night picture on an Android phone. The code is written in Python, and makes use of ADB (Android Debug Bridge) commands to interact with the device.

## Requirements
- A Android phone with Wireless/USB Debugging enabled
- ADB (Android Debug Bridge) installed on your computer
- Python 3

## Getting Started

1. Clone the repository to your local machine
```
git clone https://github.com/zkhan93/adb-photo-automation.git
```
2. Connect your Android phone to your computer
    2.1 by using a USB cable OR
    2.2 keep them on same network
   and enable USB/WiFi debugging from "developer settings" 
3. Go to the cloned repository directory and run the script

```bash
$ cd adb-photo-automation
$ python3 -m virtualenv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
(venv)$ python main.py
```

## Usage

You can also customize the script to set the number of pictures to take by adjusting the delay between each picture in `.env` file

Set the delay between pictures (in seconds)
INTERVAL=10

If you phone has a PIN lock then modify the UNLOCK_SEQ to automatically unlock it
UNLOCK_SEQ=1 2 3 4 check

## Note

This script is tested on OnePlus 6 and it's working fine, but it may not work on other devices.

## Contribution

You're welcome to contribute to this project by sending pull requests and reporting issues.

## Licence

This project is licensed under the MIT License - see the [LICENSE](https://github.com/zkhan93/adb-photo-automation/blob/master/LICENSE) file for details.

## Acknowledgments

* ADB documentation
* Python documentation
* OnePlus 6 users community
