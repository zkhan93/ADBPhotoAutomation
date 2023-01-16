# OnePlus Night Picture Automator

This repository contains code that uses ADB to automate clicking night picture on a OnePlus 6 Android phone. The code is written in Python, and makes use of ADB (Android Debug Bridge) commands to interact with the device.

## Requirements
- A OnePlus 6 Android phone with Wireless/USB Debugging enabled
- ADB (Android Debug Bridge) installed on your computer
- Python 3

## Getting Started

1. Clone the repository to your local machine
```
git clone https://github.com/zkhan93/OnePlusNightPictureAutomator.git
```
2. Connect your OnePlus 6 to your computer using a USB cable, and make sure that USB Debugging is enabled on the device.
3. Go to the cloned repository directory and run the script

```
cd OnePlusNightPictureAutomator
python main.py
```

## Usage

The script will prompt you to choose the folder where the night pictures will be saved.

Please select the folder where you want to save the pictures:

You can also customize the script to set the number of pictures to take and the delay between each picture.

Set the number of pictures to take
num_of_pics = 10

Set the delay between pictures (in seconds)
delay = 2

## Note

This script is tested on OnePlus 6 and it's working fine, but it may not work on other devices.

## Contribution

You're welcome to contribute to this project by sending pull requests and reporting issues.

## Licence

This project is licensed under the MIT License - see the [LICENSE](https://github.com/zkhan93/OnePlusNightPictureAutomator/blob/master/LICENSE) file for details.

## Acknowledgments

* ADB documentation
* Python documentation
* OnePlus 6 users community
