'''
Converts Mesen's custom .mlb format into .info files, which can be used by da65 to nicely disassemble the rom.
'''
import sys

# takes in string, returns string.
def mlb_to_info(mlb):
    mlb_lines = mlb.split('\n')[:-1]
    info = []
    for line in mlb_lines:
        tokens = line.split(':')
        # P=PRG, R=RAM, S=SRAM, W=WRAM, G=Registers. I don't think we care.
        # will have to assume everything is a bytetable for now
        addr = [int(i, 16) for i in tokens[1].split('-')]
        for i in range(len(addr)):
            if addr[i] > 0x70000:
                addr[i] -= 0x70000
            if tokens[0] == 'S':
                addr[i] += 0x6000
        size = ''
        if len(addr) > 1:
            size = f' SIZE {addr[1]-addr[0]+1};'
        comment = ''
        if len(tokens) > 3:
            comment_str = ':'.join(tokens[3:])
            comment_str = comment_str.replace('\\n', '\\n; ')
            comment = f' COMMENT "{comment_str}";'
        info.append(f'LABEL {{ ADDR ${addr[0]:04X}; '
                f'NAME "{tokens[2]}";'
                f'{size}'
                f'{comment} }};')
    return '\n'.join(info)

if __name__ == '__main__':
    mlb = ''
    with open(sys.argv[1], 'r') as f:
        mlb = f.read()
    info = mlb_to_info(mlb)
    with open('bad_apple_start.info', 'r') as f:
        start = f.read()
    with open('bad_apple.info', 'w') as f:
        f.write(start)
        f.write(info)

