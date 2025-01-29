from Dicio import inst

# Classe que realiza a montagem do código Assembly em código binário
class Assembler:
    def assemble(self, codigoAssembly):
        binary_inst = []
        for linha in codigoAssembly.strip().split("\n"):
            parts = linha.replace(",", "").split()
            if len(parts) == 0:
                continue
            simbolo = parts[0]
            if simbolo not in inst:
                raise ValueError(f"Instrução desconhecida: {simbolo}")
            binary = inst[simbolo] + " " + " ".join(parts[1:])
            binary_inst.append(binary)
        return binary_inst