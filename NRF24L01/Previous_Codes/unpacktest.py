data = [64, 240, 83, 148]
b = ''.join(chr(i) for i in data)
import struct
struct.unpack('>f', b)

