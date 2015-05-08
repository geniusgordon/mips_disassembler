#!/usr/bin/python

import sys
from instruction import Instruction

class Disassembler():
    def __init__(self):
        self.ins = []
        self.pc = 0

    def readfile(self, filename):
        buf = []
        with open(filename, "rb") as f:
            byte = f.read(1)
            while byte != "":
                word = []
                for i in range(4):
                    word.append("%02x" % ord(byte))
                    byte = f.read(1)
                buf.append(int(''.join(word), 16))
        self.pc = buf[0]
        self.ins = buf[2:]

    def disassemble(self):
        pc = self.pc
        for word in self.ins:
            _ins = Instruction(word)
            if _ins.is_branch:
                _ins.ins["imm"] = pc+4 + _ins.ins["imm"]*4
            elif _ins.is_jump:
                addr = _ins.ins["addr"]
                _ins.ins["addr"] = ((pc+4)&0xf0000000) | (addr << 2)
            print "0x%08x:\t%s" % (pc, _ins.ins_str())
            pc += 4


if __name__ == "__main__":
    d = Disassembler()
    d.readfile(sys.argv[1])
    d.disassemble()

