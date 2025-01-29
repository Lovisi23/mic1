# Classe que simula a Cache de Dados
class Cache:
    def __init__(self, size):
        self.size = size
        self.cache = {}

    def read(self, endereco):
        if endereco in self.cache:
            print(f"Cache hit: {endereco}")
            return self.cache[endereco]
        print(f"Cache miss: {endereco}")
        return None

    def write(self, endereco, valor):
        if len(self.cache) >= self.size:
            removido = next(iter(self.cache))
            print(f"Cache cheia, bloco será removido: {removido}")
            del self.cache[removido]
        self.cache[endereco] = valor
        print(f"Escrevendo na cache: {endereco} -> {valor}")