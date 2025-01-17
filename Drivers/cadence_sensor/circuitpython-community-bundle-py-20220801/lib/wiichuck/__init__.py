# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
# SPDX-FileCopyrightText: 2021 John Furcean
#
# SPDX-License-Identifier: MIT

"""
`wiichuck`
================================================================================

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


* Author(s): Carter Nelson, John Furcean

Implementation Notes
--------------------

**Hardware:**

* `Wii Remote Nunchuk <https://en.wikipedia.org/wiki/Wii_Remote#Nunchuk>`_
* `Wiichuck <https://www.adafruit.com/product/342>`_
* `Adafruit Wii Nunchuck Breakout Adapter <https://www.adafruit.com/product/4836>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
import time
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.3"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Nunchuk.git"

_I2C_INIT_DELAY = 0.1


class WiiChuckBase:  # pylint: disable=too-few-public-methods
    """
    Base Class which provides interface to Nintendo Nunchuk Accessories.

    :param i2c: The `busio.I2C` object to use.
    :param address: The I2C address of the device. Default is 0x52.
    :type address: int, optional
    :param i2c_read_delay: The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    :type i2c_read_delay: float, optional
    """

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        self.buffer = bytearray(8)
        self.i2c_device = I2CDevice(i2c, address)
        self._i2c_read_delay = i2c_read_delay
        time.sleep(_I2C_INIT_DELAY)
        with self.i2c_device as i2c_dev:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c_dev.write(b"\xF0\x55")
            time.sleep(_I2C_INIT_DELAY)
            i2c_dev.write(b"\xFB\x00")

    def _read_data(self):
        return self._read_register(b"\x00")

    def _read_register(self, address):
        with self.i2c_device as i2c:
            i2c.write(address)
            time.sleep(self._i2c_read_delay)  # at least 200us
            i2c.readinto(self.buffer)
        return self.buffer
