from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import time
import re
import logging
import ephem
from datetime import datetime
from pydantic import BaseSettings
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")



class Settings(BaseSettings):
    ip: str
    port: int
    keyfile: str
    # interval in seconds to click picture
    interval: int
    unlock_seq: list[str]

    class Config:
        env_file = ".env"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'unlock_seq':
                return raw_val.split(' ')
            return cls.json_loads(raw_val)


class AndroidDevice:
    def __init__(self, config):
        self.config = config
        self.adb = AdbDeviceTcp(config.ip, config.port, default_transport_timeout_s=9.)
        self.adb.connect(rsa_keys=[self.signer], auth_timeout_s=0.1)

    @property
    def signer(self):
        with open(self.config.adbkey) as f:
            priv = f.read()
        with open(self.config.adbkey + '.pub') as f:
            pub = f.read()
        return PythonRSASigner(pub, priv)

    def tap(self, x, y):
        return self.adb.shell(f"input tap {x} {y}")

    def press(self, keycode):
        return self.adb.shell(f"input keyevent {keycode}")
    
    def power(self, on=True):
        val = self.screen_state.startswith("on")
        while val == on:
            logger.info(f"[POWER] {on} {val}")
            self.press("KEYCODE_POWER")
            time.sleep(0.5)
            val = self.screen_state.startswith("on")

    def swipe(self, direction, longx=1, from_end=False, dx=0, dy=0):
        length = int(280 * longx)
        
        x1 = {
            "up": 530, "down": 530, "right": 30 if from_end else 220 , "left": 1070 if from_end else 820
        }[direction]
        y1 = {
            "up": 2278 if from_end else 1700, "down": 112 if from_end else 1150, "right": 1100, "left": 1100 
        }[direction]
        x2 = {
            "up": x1, "down": x1, "right": x1 + length, "left": x1 - length
        }[direction]
        y2 = {
            "up": y1 - length , "down": y1 + length, "right": y1 , "left": y1
        }[direction]
        print(f"{x1 + dx} {y1 + dy} => {x2+dx} {y2+dy}")
        self.adb.shell(f"input touchscreen swipe {x1+dx} {y1+dy} {x2+dx} {y2+dy} 200")

    
    def close_app(self):
        self.swipe("up", from_end=True)

    def unlock(self):
        numpad = {
            "1": (240, 890),
            "2": (550, 890),
            "3": (840, 890),
            "4": (240, 1100),
            "5": (550, 1100),
            "6": (840, 1100),
            "7": (240, 1300),
            "8": (550, 1300),
            "9": (840, 1300),
            "del": (240, 1500),
            "0": (550, 1500),
            "check": (840, 1500)
        }
        for seq in self.config.unlock_seq:
            xy = numpad.get(seq)
            if xy:
                self.tap(xy[0], xy[1])
            else:
                logger.error(f"unknown key {seq}")
        

    def open_cam(self):
        mode = "photo" if is_lights_on() else "pro"
        self.adb.shell("am start -a android.media.action.STILL_IMAGE_CAMERA")
        time.sleep(2)
        self._set_cam_mode(mode)
        time.sleep(1)
        return mode
      
    def take_pic(self):
        val = self.adb.shell("ls /sdcard/DCIM/Camera/ | wc -l")
        self.tap(540,1980)
        # wait till a new file is created in camera
        while val == self.adb.shell("ls /sdcard/DCIM/Camera/ | wc -l"):
            time.sleep(1)

    def _set_cam_mode(self, mode="photo"):
        # open menu
        self.swipe("up")
        y = {
            "pro": 1660,
            "photo": 1290
        }[mode]
        self.tap(540, y)
        time.sleep(0.5)
        if mode == "pro":
            self._set_iso()
            self._set_shutter()
            self._set_focus()
        time.sleep(0.3)

    def _set_iso(self):
        # iso
        self.tap(133, 1560)
        self.swipe("right", longx=3, dy=140, dx=-150)
        self.swipe("right", longx=3, dy=140)
        self.tap(133, 1560)
        
    def _set_shutter(self):
        self.tap(520, 1560)
        self.swipe("left", longx=3, dy=140, dx=210)
        self.swipe("left", longx=3, dy=140, dx=210)
        self.tap(520, 1560)

    def _set_focus(self):
        self.tap(730, 1550)
        self.swipe("left", longx=3, dy=140, dx=200)
        self.tap(730, 1550)
    
    @property
    def battery_info(self):
        info = {}
        for line in self.adb.shell("dumpsys battery").strip().split('\n'):
            if line:
                k, v = re.split(r":\s*", line, maxsplit=1)
                info[k.strip().lower()] = v
        return info

    @property
    def battery_level(self):
        return float(self.battery_info.get("level", -1))

    @property
    def screen_state(self):
        res = self.adb.shell("dumpsys nfc | grep 'mScreenState='")
        if res and '=' in res:
            return res.strip().split('=')[1].lower()
        return ""

    def process1(self):
        """Open camera and take pic"""
        logger.info(f"screen_state: '{self.screen_state}'")
        if self.screen_state.startswith("off"):
            logger.info("screen is off, turning it on")
            self.power(True)
        else:
            logger.info("screen is on")
        if not self.screen_state.endswith("unlocked"):
            logger.info("phone is locked, unlocking")
            self.swipe("up")
            time.sleep(0.5)
            self.unlock()
        else:
            logger.info("phone is unlocked, proceeding")
        time.sleep(1)
        # self.close_app()
        self.open_cam()
        self.take_pic()
        self.close_app()
        self.power(False)
        

def is_lights_on():
    sun = ephem.Sun()
    city = ephem.Observer()
    city.name = "Grand Cayman"
    city.lat, city.lon, city.elevation = (19.317631, -81.181647, 13.0)
    city.compute_pressure()
    sun.compute(city)
    twilight = -12 * ephem.degree
    logger.info(f"Is it light in Grand Cayman right now ? {datetime.utcnow().isoformat()} {sun.alt > twilight}")
    return sun.alt > twilight

def main():
    config = Settings()
    logger.info(config)
    dev = AndroidDevice(config)
    while True:
        try:
            start = time.time()
            dev.process1()
        except Exception:
            logger.exception("process1 failed")
        finally:
            dev.power(False)
        time_taken = time.time() - start
        sleep_for = max(int(config.interval - time_taken), 0)
        logger.info(f"took: {time_taken} sleeping for {sleep_for}..")
        time.sleep(sleep_for)

if __name__ == "__main__":
    main()