
def getVideoOpcode(opcode):
    mode = (opcode & 0xC0) >> 6
    data = opcode & 0x3F
    return mode, data

# mode 3
def patchNametablePage():
    pass

# mode 2
def copyEntireNametable():
    pass

# mode 1
def freezeFrame():
    pass

# mode 0
def resetVideo():
    pass

def processVideoInstruction(ptr):
    mode, data = getVideoOpcode(ptr)

