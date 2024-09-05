
"""
Author: Varun Kumar
Organization: TU/e
Date: 2024-09-03
Description:
Photo frame viewer for Raspberry Pi 4 and 5

Hardware required:
- 2.4" SPI TFT display with ILI9341 Driver

SPI interface must be enabled!
To do this, execute the following command and then reboot the device:
sudo sed -i '/^#dtparam=spi=on/s/^#//' /boot/firmware/config.txt
sudo reboot

License: GPL-3.0 license
Contact: varunkumar@gmail.com

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import time
import digitalio
import board
from PIL import Image, ImageOps
from adafruit_rgb_display import ili9341

# RPI pinout
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D27)

backlight = digitalio.DigitalInOut(board.D18)
backlight.switch_to_output()
backlight.value = True

# Config for display baudrate (default max is 64mhz):
BAUDRATE = 64000000
ROTATION = 90

# Setup SPI bus using hardware SPI:
spi = board.SPI()

display = ili9341.ILI9341(spi, rotation=ROTATION, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

# Image folder
image_width = 240
image_height = 320
folder = "images"

if ROTATION % 180 == 90:
    image_height, image_width = image_width, image_height  # we swap height/width to rotate it to landscape!

# loop over files in directory
if folder is not None:
    print("Entering directory....")
    while True:
        for image_files in os.listdir(folder):
            image_file = os.path.join(folder, image_files)
            image = Image.open(image_file)
            image_frame = ImageOps.pad(image.convert("RGB"), (image_width, image_height), method=Image.NEAREST, color=(0,0,0), centering=(0.5, 0.5),)
            display.image(image_frame)
            time.sleep(10)
