from time import sleep_ms
from machine import I2C, Pin
from i2c_lcd import I2cLcd

DEFAULT_I2C_ADDR = 60


def test_main():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    for s in range(3, 0, -1):
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(
            "Conected at {}\n"
            "Light test in {}".format(DEFAULT_I2C_ADDR, s)
        )
        sleep_ms(1000)

    for s in range(3, 0, -1):
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(
            "Light test On\n"
            "Off in {}".format(s)
        )
        sleep_ms(500)
        lcd.backlight_off()
        sleep_ms(500)
        lcd.backlight_on()

    lcd.display_off()
    lcd.clear()


test_main()
