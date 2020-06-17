"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4  # stack pointer
        self.pc = 0
        self.sp = self.reg[7]
        self.instructions = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b01100101: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,
            0b01000101: self.push,
            0b01000110: self.pop
        }

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
        address = 0

        with open(program_name) as p:
            for line in p:
                line = line.split("#")[0]

                try:
                    instruction = int(line, 2)
                except ValueError:
                    continue

                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

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
            instruction = self.instructions.get(ir)

            if instruction:
                self.instructions[ir]()

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
        sys.exit(0)

    def add(self):
        addresses = self.get_operands()

        self.alu("ADD", *addresses)
        self.pc += 3

    def sub(self):
        addresses = self.get_operands()

        self.alu("SUB", *addresses)
        self.pc += 3

    def mul(self):
        addresses = self.get_operands()

        self.alu("MUL", *addresses)
        self.pc += 3

    def div(self):
        addresses = self.get_operands()

        self.alu("DIV", *addresses)
        self.pc += 3

    def get_operands(self):
        address_1 = self.ram[self.pc+1]
        address_2 = self.ram[self.pc+2]

        return [address_1, address_2]

    def push(self):
        self.sp -= 1

        address = self.ram[self.pc+1]
        value = self.reg[address]
        self.ram[self.sp] = value

        self.pc += 2

    def pop(self):
        address = self.ram[self.pc+1]
        value = self.ram[self.sp]
        self.reg[address] = value

        self.sp += 1
        self.pc += 2
