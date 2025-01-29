import tkinter as tk
from Assembler import Assembler
from Simulador import Simulador

# Classe da interface gráfica (GUI)
class GrafInterface:
    def __init__(self, root):
        def attLabelRegistrador(reg, valor):
            self.register_labels[reg].config(text=f"R{reg}: {valor}")

        self.sim = Simulador(attDeRegistrador=attLabelRegistrador)
        self.assembler = Assembler()

        root.title("Simulador MIC-1")

        # Layout principal
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Layout do código Assembly
        assembly_frame = tk.LabelFrame(main_frame, text="Código Assembly", padx=10, pady=10)
        assembly_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.assembly_input = tk.Text(assembly_frame, height=10, width=40)
        self.assembly_input.pack()
        
        button_frame = tk.Frame(assembly_frame)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Carregar", command=self.load_code).pack(side="left", padx=5)
        tk.Button(button_frame, text="Próximo", command=self.next_instruction).pack(side="left", padx=5)
        tk.Button(button_frame, text="Limpar", command=self.clear_all).pack(side="left", padx=5)

        # Layout dos registradores
        reg_frame = tk.LabelFrame(main_frame, text="Registradores", padx=10, pady=10)
        reg_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.register_labels = []
        for i in range(8):
            label = tk.Label(reg_frame, text=f"R{i}: 0", width=15, anchor="w")
            label.pack(anchor="w")
            self.register_labels.append(label)

        # Layout da memória e cache
        memory_frame = tk.LabelFrame(main_frame, text="Memória e Cache", padx=10, pady=10)
        memory_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.memory_display = tk.Text(memory_frame, height=20, width=80)
        self.memory_display.pack()

        # Status
        self.status_label = tk.Label(main_frame, text="Status: Aguardando execução", fg="blue")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

    def load_code(self):
        codigoAssembly = self.assembly_input.get("1.0", tk.END).strip()
        print(f"Código Assembly recebido:\n{codigoAssembly}")

        try:
            binary_inst = self.assembler.assemble(codigoAssembly)
            print(f"Instruções montadas:\n{binary_inst}")

            self.sim.load_instructions(binary_inst)
            self.memory_display.delete("1.0", tk.END)
            self.memory_display.insert(tk.END, "Código carregado! Clique em Próximo para executar.\n")
            self.status_label.config(text="Status: Código carregado", fg="green")
        except Exception as e:
            self.memory_display.delete("1.0", tk.END)
            self.memory_display.insert(tk.END, f"Erro: {str(e)}")
            self.status_label.config(text="Status: Erro ao carregar código", fg="red")

    def next_instruction(self):
        try:
            result = self.sim.execute_next()
            if result == "Fim":
                self.memory_display.insert(tk.END, "Execução finalizada!\n")
                self.status_label.config(text="Status: Execução finalizada", fg="green")
                return

            self.memory_display.delete("1.0", tk.END)
            self.memory_display.insert(tk.END, "Cache de Dados:\n")
            for endereco, valor in self.sim.data_cache. cache.items():
                self.memory_display.insert(tk.END, f"Endereço 0x{endereco:02X}: {valor}\n")
            self.memory_display.insert(tk.END, "\nMemória:\n")
            for i, valor in enumerate(self.sim.memory):
                if valor != 0:
                    self.memory_display.insert(tk.END,f"Endereço 0x{i:02X}: {valor}\n")

            self.memory_display.insert(tk.END, "\nRegistradores:\n")
            for i in range(8):
                self.memory_display.insert(tk.END, f"R{i}: {self.sim.reg[i]}\n")

            self.status_label.config(text="Status: Próxima instrução executada", fg="blue")
        except Exception as e:
            self.memory_display.insert(tk.END, f"Erro: {str(e)}\n")
            self.status_label.config(text="Status: Erro na execução", fg="red")

    def clear_all(self):
        self.assembly_input.delete("1.0", tk.END)
        for i in range(8):
            self.register_labels[i].config(text=f"R{i}: 0")
        self.memory_display.delete("1.0", tk.END)
        self.sim = Simulador(attDeRegistrador=lambda reg, valor: self.register_labels[reg].config(text=f"R{reg}: {valor}"))
        self.status_label.config(text="Status: Limpo", fg="blue")

# Inicia a interface gráfica
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = GrafInterface(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro: {e}")