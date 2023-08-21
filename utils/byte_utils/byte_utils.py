def pad_number_with_leading_zeros_to_2048(number):
    binary = '{0:02048b}'.format(number)
    b = bytearray()
    index = 0
    while index + 8 <= 2048:
        binaries = binary[index: index + 8]
        byte = int(binaries, 2)
        b.append(byte)
        index = index + 8
    return bytes(b)
