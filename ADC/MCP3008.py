def read_adc(adc_num):
    spi = machine.SPI(1)
    spi.init(baudrate=1000000, phase=0, polarity=0)

    cs = machine.Pin(15, machine.Pin.OUT)
    # Make sure CS line starts high
    cs.on()
    cs.off()

    command = adc_num
    command |= 8
    command <<= 4
    # Start Byte, Command Byte, Don't Care Byte
    b_array = bytearray([1, command, 0xFF])
    spi.write_readinto(b_array, b_array)

    val = (b_array[1] & 3) << 8
    val |= b_array[2]

    return val