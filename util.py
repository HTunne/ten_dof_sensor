def twos_complement(a, bits):
    """ Return twos complement value of int a for a bit length bits """
    sign_bit = a & (1 << bits - 1)
    return (a & (sign_bit-1)) - (a & sign_bit)
