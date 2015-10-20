"""
This program handles the communication over I2C
between a Raspberry Pi and an ADXL345 Accelerometer
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright 2015
"""

import smbus


class ADXL345:
    # Global Variables
    EARTH_GRAVITY_MS2 = 9.80665
    GRAVITY_MS2 = None
    # This is the typical scale factor in g/LSB as given in the datasheet (page 4)
    SCALE_MULTIPLIER = 0.0039
    # This is the bus that we use to send data over I2C
    bus = smbus.SMBus(1)
    address = None
    DEBUG = False

    # ADXL345 Registers
    DATA_FORMAT = 0x31
    BANDWIDTH_RATE_REG = 0x2C
    POWER_CTL = 0x2D
    measure = 0x08

    BANDWIDTH_RATE_1600HZ = 0x0F
    BANDWIDTH_RATE_800HZ = 0x0E
    BANDWIDTH_RATE_400HZ = 0x0D
    BANDWIDTH_RATE_200HZ = 0x0C
    BANDWIDTH_RATE_100HZ = 0x0B
    BANDWIDTH_RATE_50HZ = 0x0A
    BANDWIDTH_RATE_25HZ = 0x09

    RANGE_2G = 0x00
    RANGE_4G = 0x01
    RANGE_8G = 0x02
    RANGE_16G = 0x03

    DATAX0 = 0x32
    DATAX1 = 0x33
    DATAY0 = 0x34
    DATAY1 = 0x35
    DATAZ0 = 0x36
    DATAZ1 = 0x37

    def __init__(self,  address, base_range = RANGE_2G, base_bandwidth_rate = BANDWIDTH_RATE_100HZ):
        self.GRAVITY_MS2 = self.EARTH_GRAVITY_MS2
        self.address = address
        self.set_bandwidth_rate(base_bandwidth_rate)
        self.set_range(base_range)
        self.enable_measurement()

    def enable_measurement(self):
        """Enables measurement by writing 0x08 to POWER_CTL."""
        try:
            self.bus.write_byte_data(self.address, self.POWER_CTL, self.measure)
        except:
            print("Error in enable_measurement(), are you sure that the ADXL345 is wired correctly?")

    def disable_measurement(self):
        """Disables measurement by writing 0x00 to POWER_CTL."""
        try:
            self.bus.write_byte_data(self.address, self.POWER_CTL, 0x00)
        except:
            print("Error in disable_measurement(), are you sure that the ADXL345 is wired correctly?")

    def read_measurement_mode(self):
        """Reads POWER_CTL.

        Returns the read value.
        """
        try:
            return self.bus.read_byte_data(self.address, self.POWER_CTL)
        except:
            print("Error in read_measurement_mode(), are you sure that the ADXL345 is wired correctly?")

    def set_bandwidth_rate(self, rate):
        """Changes the bandwidth rate by writing rate to BANDWIDTH_RATE_REG.

        rate -- the bandwidth rate the ADXL345 will be set to. Using a pre-defined rate is advised.
        """
        try:
            self.bus.write_byte_data(self.address, self.BANDWIDTH_RATE_REG, rate)
        except:
            print("Error in set_bandwidth_rate(), are you sure that the ADXL345 is wired correctly?")

    def read_bandwidth_rate(self):
        """Reads BANDWIDTH_RATE_REG.

        Returns the read value.
        """
        try:
            raw_bandwidth_rate = self.bus.read_byte_data(self.address, self.bandwidthRate)
            return raw_bandwidth_rate & 0x0F
        except:
            print("Error in read_bandwidth_rate, are you sure that the ADXL345 is wired correctly?")

    # Changes the range of the ADXL345. Available ranges are 2G, 4G, 8G and 16G.
    def set_range(self, range):
        """Changes the range of the ADXL345.

        range -- the range to set the accelerometer to. Using a pre-defined range is advised.
        """
        value = None
        
        try:
            value = self.bus.read_byte_data(self.address, self.DATA_FORMAT)
        except:
            print("Error in read_bandwidth_rate, are you sure that the ADXL345 is wired correctly?")
            return

        value &= ~0x0F;
        value |= range;
        value |= 0x08;

        self.bus.write_byte_data(self.address, self.DATA_FORMAT, value)

    def read_range(self, hex):
        """Reads the range the ADXL345 is currently set to.

        hex -- If hex is true it wil return a hexadecimal value. If raw is false it will return a string.
        """
        raw_value = self.bus.read_byte_data(self.address, self.DATA_FORMAT)

        if hex is True:
            if raw_value == 8:
                return self.RANGE_2G
            elif raw_value == 9:
                return self.RANGE_4G
            elif raw_value == 10:
                return self.RANGE_8G
            elif raw_value == 11:
                return self.RANGE_16G
        elif hex is False:
            if raw_value == 8:
                return "2G"
            elif raw_value == 9:
                return "4G"
            elif raw_value == 10:
                return "8G"
            elif raw_value == 11:
                return "16G"

    def get_all_axes(self, round = False):
        """Gets the measurement results from all the axes.

        round -- if round is true it will round to 4 digits.
        Returns a dictionary.
        """
        # Read the raw bytes from the ADXL345
        bytes = self.bus.read_i2c_block_data(self.address, self.DATAX0, 6)

        # bit shifting magic.
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1 << 16)
        
        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1 << 16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1 << 16)

        # Multiply the values by the scale multiplier to get the acceleration in g. 
        # The scale multiplier is given in the datasheet.
        x = x * self.SCALE_MULTIPLIER
        y = y * self.SCALE_MULTIPLIER
        z = z * self.SCALE_MULTIPLIER
        
        # Multiply the values in g by the gravity in m/s^2 to get the acceleration in m/s^2.
        x = x * self.GRAVITY_MS2
        y = y * self.GRAVITY_MS2
        z = z * self.GRAVITY_MS2

        # Round the values if the user wants to
        if round == True:
            x = round(x, 4)
            y = round(y, 4)
            z = round(z, 4)

        # Return the correct values
        if self.DEBUG == False:
            return {"x": x, "y": y, "z": z}
        elif self.DEBUG == True:
            return {"x": x, "y": y, "z": z, "bytes": bytes}
        else:
            return {"x": x, "y": y, "z": z}

    def get_one_value(self, value, round = False):
        """Reads one value and returns it.

        value -- the value to be read. this can be 'x', 'y' or 'z'.
        """
        read_register = 0x00
        
        if value == 'x':
            read_register = self.DATAX0
        elif value == 'y':
            read_register = self.DATAY0
        elif value == 'z':
            read_register = self.DATAZ0
            
        # Read the raw bytes from the ADXL345
        bytes = self.bus.read_i2c_block_data(self.address, read_register, 2)

        # bit shifting magic.
        val = bytes[0] | (bytes[1] << 8)
        if(val & (1 << 16 - 1)):
            val = val - (1 << 16)
            
        # Multiply the value by the scale multiplier to get the acceleration in g.
        val = val * self.SCALE_MULTIPLIER

        # Multiply the value in g by the gravity in m/s^2 to get the acceleration in m/s^2.
        val = val * self.GRAVITY_MS2
        
        # Round the values if the user wants to
        if round == True:
            val = round(val, 4)
        
        return val

# If a user runs this file just display the latest values
if __name__ == "__main__":
    accelerometer = ADXL345(0x53)
    axes = accelerometer.get_all_axes()
    print("x: %.3f" % (axes['x']))
    print("y: %.3f" % (axes['y']))
    print("z: %.3f" % (axes['z']))
