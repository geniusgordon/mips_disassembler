r_type_ins = [
    {
        0x20: "ADD",
        0x22: "SUB",
        0x24: "AND",
        0x25: "OR",  
        0x26: "XOR", 
        0x27: "NOR", 
        0x28: "NAND",
        0x2A: "SLT", 
        "format": "%s\t$%d, $%d, $%d",
        "oprand": ["rd", "rs", "rt"],
    },
    {
        0x00: "SLL", 
        0x02: "SRL", 
        0x03: "SRA", 
        "format": "%s\t$%d, $%d, %d",
        "oprand": ["rd", "rs", "shamt"],
    },
    {
        0x08: "JR",  
        "format": "%s\t$%d",
        "oprand": ["rs"],
    }
]
i_type_ins = [
    {
        0x08: "ADDI",
        0x0a: "SLTI", 	
        "format": "%s\t$%d, $%d, %d",
        "oprand": ["rt", "rs", "imm"],
    },
    {
        0x0c: "ANDI", 	
        0x0d: "ORI", 	
        0x0e: "NORI", 	
        "format": "%s\t$%d, $%d, %d",
        "oprand": ["rt", "rs", "immu"],
    },
    {
        0x23: "LW", 	
        0x21: "LH", 	
        0x25: "LHU", 	
        0x20: "LB", 	
        0x24: "LBU", 	
        0x2b: "SW", 	
        0x29: "SH", 	
        0x28: "SB", 	
        "format": "%s\t$%d, %d($%d)",
        "oprand": ["rt", "imm", "rs"],
    },
    {
        0x0f: "LUI", 	
        "format": "%s\t$%d, %d",
        "oprand": ["rt", "immu"],
    }
]
branch = {
    0x04: "BEQ", 	
    0x05: "BNE", 	
    "format": "%s\t$%d, $%d, 0x%08x",
    "oprand": ["rs", "rt", "imm"],
}
jump = {
    0x02: "J",
    0x03: "JAL",
    "format": "%s\t0x%08x",
    "oprand": ["addr"],
}

def extract(value, left, right):
    mask = 0xffffffff
    return (value >> right) & (mask >> (31-left+right))

def sign_extension(value, bits):
    if value & (1 << bits-1) != 0:
        value |= (extract(0xffffffff, 31, bits) << bits)
    return value

class Instruction():
    def __init__(self, ins_hex=0):
        self.ins = {}
        self.ins_hex = ins_hex
        self.name = ""
        self.is_branch = False
        self.is_jump = False
        self.decode()

    def decode(self):
        self.ins["op"] = extract(self.ins_hex, 31, 26)
        self.ins["rs"] = extract(self.ins_hex, 25, 21)
        self.ins["rt"] = extract(self.ins_hex, 20, 16)
        self.ins["rd"] = extract(self.ins_hex, 15, 11)
        self.ins["shamt"] = extract(self.ins_hex, 10, 6)
        self.ins["funct"] = extract(self.ins_hex, 5, 0)
        self.ins["imm"] = sign_extension(extract(self.ins_hex, 15, 0), 16)
        self.ins["immu"] = extract(self.ins_hex, 15, 0)
        self.ins["addr"] = extract(self.ins_hex, 25, 0)

        if self.ins["op"] == 0:
            for _r in r_type_ins:
                if self.ins["funct"] in _r:
                    self.name = _r[self.ins["funct"]]
                    self.ins_format = _r["format"]
                    self.ins_oprand = _r["oprand"]
        else:
            for _i in i_type_ins:
                if self.ins["op"] in _i:
                    self.name = _i[self.ins["op"]]
                    self.ins_format = _i["format"]
                    self.ins_oprand = _i["oprand"]
            if self.ins["op"] in jump:
                self.name = jump[self.ins["op"]]
                self.ins_format = jump["format"]
                self.ins_oprand = jump["oprand"]
                self.is_jump = True
            if self.ins["op"] in branch:
                self.name = branch[self.ins["op"]]
                self.ins_format = branch["format"]
                self.ins_oprand = branch["oprand"]
                self.is_branch = True
            if self.ins["op"] == 0x3f:
                self.name = "HALT"
                self.ins_format = "%s"
                self.ins_oprand = []

        if self.name == "":
            print self.ins
            raise Exception("Unknown Instruction 0x%08x\n" % self.ins_hex)

    def ins_str(self):
        t = (self.name,) + tuple([self.ins[x] for x in self.ins_oprand])
        return self.ins_format % t

