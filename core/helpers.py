class ShiftRegister:
    """ SPI Shift Register interface """

    def __init__(self, spi, latch_pin):
        self.spi = spi
        self.latch = latch_pin

    def shift(self, buf):
        self.spi.write(buf)
        self.latch.on()
        self.latch.off()
