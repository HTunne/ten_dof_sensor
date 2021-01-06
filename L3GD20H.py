from ten_dof_sensor.util import twos_complement

class L3GD20H:
    '''Class to control the L3GD20H 3-axis gryoscope module via I2C protocol in micropython'''
    def __init__(self, I2C_object, address_LSb = 1):
        self.address = 0b1101010 | address_LSb
        self.I2C_object = I2C_object
        self._define_register_addresses()
        self._define_bytearrays()
        self._sensitivity = 0.00875

        # initialise device
        self.set_mode_normal()

    def _define_register_addresses(self):
        self.registers = {
            "WHO_AM_I": 0b0001111,
            "CTRL1": 0b0100000,
            "OUT_X_L": 0b0101000,
            "OUT_X_H": 0b0101001,
            "OUT_Y_L": 0b0101010,
            "OUT_Y_H": 0b0101011,
            "OUT_Z_L": 0b0101100,
            "OUT_Z_H": 0b0101101
        }

    def _define_bytearrays(self):
        self.byte_H = bytearray(1)
        self.byte_L = bytearray(1)
        self.byte_CTRL1 = bytearray(1)

    def _read_OUT_register(self, L__reg_address, H__reg_address):
        self.I2C_object.readfrom_mem_into(self.address, L__reg_address, self.byte_L)
        self.I2C_object.readfrom_mem_into(self.address, H__reg_address, self.byte_H)

        return twos_complement((self.byte_H[0] << 8) | self.byte_L[0], 16)

    def who_am_i(self):
        return self.I2C_object.readfrom_mem(self.address, self.registers["WHO_AM_I"], 1) == b'\xd7'

    def read_gyro(self):
        x = self._read_OUT_register(self.registers["OUT_X_L"], self.registers["OUT_X_H"]) * self._sensitivity
        y = self._read_OUT_register(self.registers["OUT_Y_L"], self.registers["OUT_Y_H"]) * self._sensitivity
        z = self._read_OUT_register(self.registers["OUT_Z_L"], self.registers["OUT_Z_H"]) * self._sensitivity

        return (x, y, z)

    def set_mode_normal(self):
        self.I2C_object.writeto_mem(self.address, self.registers["CTRL1"], b'\x0f')

    def set_mode_power_down(self):
        self.I2C_object.writeto_mem(self.address, self.registers["CTRL1"], b'\x00')

    def set_mode_sleep(self):
        self.I2C_object.writeto_mem(self.address, self.registers["CTRL1"], b'\x08')

    # add who am i check in init
    # look at changing range
