compBytes1 = bytearray(b'\xf2\xea\x82\x36\x8e\x12\x18\x73\x7b\x11\x5b\x69\x38\x8a\xb0\x8b\x8e\x83\xf6\xc4\x39\xf5\xa2')
compBytes2 = bytearray(b'\x9c\xd9\xf5\x69\xef\x75\x2b\x2c\x0d\x20\x29\x1d\x4d\xbe\xdc\xe2\xf4\xb7\x82\xf5\x56\x9b\xfd')

for i in range(0,len(compBytes1)):
    print(chr(compBytes1[i]^compBytes2[i]), end='')