from ADC.MCP3008 import read_adc


def get_co_percentage(pin):
    co_val = read_adc(pin)
    co_per = co_val / 1024.0

    return co_per
