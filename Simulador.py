from Cache import Cache

# Classe principal do simulador
class Simulador:
    def __init__(self, attDeRegistrador=None):
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.data_cache = Cache(4)
        self.attDeRegistrador = attDeRegistrador
        self.instructions = []
        self.pc = 0
        self.stack_pointer = 0xFF  # Ponteiro de pilha
        self.flags = {"Z": 0, "C": 0}

    def attReg(self, reg, valor):
        self.reg[reg] = valor & 0xFF
        if self.attDeRegistrador:
            self.attDeRegistrador(reg, valor & 0xFF)

    def set_flag(self, flag, valor):
        self.flags[flag] = valor

    def load_instructions(self, instructions):
        self.instructions = instructions
        self.pc = 0

    def execute_next(self):
        if self.pc >= len(self.instructions):
            return "Fim"

        instruction = self.instructions[self.pc]
        print(f"Executando instrução: {instruction}")
        parts = instruction.split()
        opcode = parts[0]

        if opcode == '0000':  # LODD
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16)  # endereços em hexadecimal
            cached_valor = self.data_cache.read(endereco)
            if cached_valor is None:
                valor = self.memory[endereco]
                self.data_cache.write(endereco, valor)
            else:
                valor = cached_valor
            self.attReg(reg, valor)

        elif opcode == '0001':  # STOD
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16)  # endereços em hexadecimal
            self.memory[endereco] = self.reg[reg]
            self.data_cache.write(endereco, self.reg[reg])

        elif opcode == '0010':  # ADDD
            reg1 = int(parts[1][1:])  # 'R0' -> 0
            reg2 = int(parts[2][1:])  # 'R1' -> 1
            valor = self.reg[reg1] + self.reg[reg2]
            self.set_flag("C", int(valor > 255))
            self.set_flag("Z", int(valor == 0))
            self.attReg(reg1, valor)

        elif opcode == '0011':  # SUBD
            reg1 = int(parts[1][1:])  # 'R0' -> 0
            reg2 = int(parts[2][1:])  # 'R1' -> 1
            valor = self.reg[reg1] - self.reg[reg2]
            self.set_flag("Z", int(valor == 0))
            self.attReg(reg1, valor)

        elif opcode == '0111':  # LOCO
            reg = int(parts[1][1:])  # 'R0' -> 0
            valor = int(parts[2], 16)  # Carregar valor imediato
            self.attReg(reg, valor)

        elif opcode == '1000':  # LODL
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16) + self.reg[reg]  # Endereço + valor do registrador
            cached_valor = self.data_cache.read(endereco)
            if cached_valor is None:
                valor = self.memory[endereco]
                self.data_cache.write(endereco, valor)
            else:
                valor = cached_valor
            self.attReg(reg, valor)

        elif opcode == '1001':  # STODL
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16) + self.reg[reg]  # Endereço + valor do registrador
            self.memory[endereco] = self.reg[reg]
            self.data_cache.write(endereco, self.reg[reg])

        elif opcode == '1010':  # ADDL
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16) + self.reg[reg]  # Endereço + valor do registrador
            valor = self.memory[endereco] + self.reg[reg]
            self.set_flag("C", int(valor > 255))
            self.set_flag("Z", int(valor == 0))
            self.attReg(reg, valor)

        elif opcode == '1011':  # PUSHI
            valor = int(parts[1], 16)  # Carregar valor imediato
            self.memory[self.stack_pointer] = valor
            self.stack_pointer -= 1
            print(f"Pushed {valor} to stack at {self.stack_pointer+1}")

        elif opcode == '1101':  # POPI
            self.stack_pointer += 1
            valor = self.memory[self.stack_pointer]
            self.attReg(0, valor)  # Desempilha para o registrador R0
            print(f"Popped {valor} from stack at {self.stack_pointer}")

        elif opcode == '1111':  # INSP
            self.stack_pointer += 1
            print(f"Stack pointer incremented to {self.stack_pointer}")

        elif opcode == '0100':  # JPOS
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16)  # endereços em hexadecimal
            if self.reg[reg] > 0:
                self.pc = endereco
                print(f"JPOS: Saltou para {endereco}")

        elif opcode == '0101':  # JZER
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16)  # endereços em hexadecimal
            if self.reg[reg] == 0:
                self.pc = endereco
                print(f"JZER: Saltou para {endereco}")

        elif opcode == '1100':  # JNEG
            reg = int(parts[1][1:])  # 'R0' -> 0
            endereco = int(parts[2], 16)  # endereços em hexadecimal
            if self.reg[reg] < 0:
                self.pc = endereco
                print(f"JNEG: Saltou para {endereco}")

        elif opcode == '0110':  # JUMP
            endereco = int(parts[1], 16)  # endereços em hexadecimal
            self.pc = endereco
            print(f"JUMP: Saltou para {endereco}")

        # Incrementa o contador de programa
        self.pc += 1
        return "Executando próxima instrução"




