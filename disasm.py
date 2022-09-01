#!/usr/bin/env python3
import subprocess
import sys

# Only part that's actual code is found starting at 516112 in the .nes and is 8192 bytes long.

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify a .nes file')
        sys.exit(1)
    rom_path = sys.argv[1]
    with open(rom_path, 'rb') as f:
        rom = f.read()
    code_bin = rom[516112:524304]
    with open('bad_apple.bin', 'wb') as f:
        f.write(code_bin)
    code = subprocess.check_output([
        'da65',
        'bad_apple.bin',
        '-i',
        'bad_apple.info'
        ])
    with open('src/bad_apple.s', 'wb') as f:
        f.write(code)

