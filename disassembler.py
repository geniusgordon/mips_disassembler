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
        for _ins in self.ins:
            print "0x%08x:\t%s" % (pc, Instruction(_ins).ins_str())
            pc += 4


if __name__ == "__main__":
    d = Disassembler()
    d.readfile(sys.argv[1])
    d.disassemble()

