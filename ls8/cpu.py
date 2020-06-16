"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def load(self):
        """Load a program into memory."""
        # check input
        if len(sys.argv) < 2:
            raise NameError("No input program specified, exiting...")

        program_name = sys.argv[1]

        with open(program_name) as p:
            for address, line in enumerate(p):
                line = line.split("#")[0]

                try:
                    instruction = int(line, 2)
                except ValueError:
                    continue

                self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running == True:
            ir = self.ram[self.pc]

            if ir == self.LDI:
                self.ldi()

            elif ir == self.PRN:
                self.prn()

            elif ir == self.MUL:
                self.mul()

            elif ir == self.HLT:
                running = self.hlt()

    def ldi(self):
        address = self.ram[self.pc+1]
        value = self.ram[self.pc+2]
        self.reg[address] = value
        self.pc += 3

    def prn(self):
        address = self.ram[self.pc+1]
        value = self.reg[address]
        print(value)
        self.pc += 2

    def hlt(self):
        self.pc += 1
        return False

    def mul(self):
        address_1 = self.ram[self.pc+1]
        address_2 = self.ram[self.pc+2]

        value_1 = self.reg[address_1]
        value_2 = self.reg[address_2]
        self.reg[address_1] = value_1 * value_2

        self.pc += 3
