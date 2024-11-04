from datetime import datetime

# Definição de um evento (depósito ou retirada)
class Evento:
    def __init__(self, tipo, valor, usuario, data=None):
        self.tipo = tipo  # "deposito" ou "retirada"
        self.valor = valor
        self.usuario = usuario
        self.data = data if data else datetime.now()

    def __str__(self):
        return f"{self.tipo.capitalize()} de {self.valor} por {self.usuario} em {self.data}"

# Classe para a Conta Bancária
class ContaBancaria:
    def __init__(self):
        self.saldo = 0  # Saldo inicial da conta
        self.eventos = []  # Lista de eventos (transações)

    def depositar(self, valor, usuario):
        """Realiza um depósito e registra o evento."""
        evento = Evento(tipo="deposito", valor=valor, usuario=usuario)
        self.eventos.append(evento)  # Registra o evento
        self.aplicar_eventos()  # Aplica o evento ao saldo

    def retirar(self, valor, usuario):
        """Realiza uma retirada se o saldo for suficiente e registra o evento."""
        if valor <= self.saldo:
            evento = Evento(tipo="retirada", valor=valor, usuario=usuario)
            self.eventos.append(evento)  # Registra o evento
            self.aplicar_eventos()  # Aplica o evento ao saldo
        else:
            print(f"Falha na retirada de {valor}. Saldo insuficiente.")

    def aplicar_eventos(self):
        """Aplica todos os eventos registrados no saldo da conta."""
        self.saldo = 0  # Reinicia o saldo antes de aplicar os eventos
        for evento in self.eventos:
            if evento.tipo == "deposito":
                self.saldo += evento.valor
            elif evento.tipo == "retirada":
                self.saldo -= evento.valor

    def reconstruir_saldo(self):
        """Reconstrói o saldo a partir do histórico de eventos."""
        self.aplicar_eventos()

    def historico_eventos(self):
        """Retorna o histórico de eventos."""
        return [str(evento) for evento in self.eventos]

    def __str__(self):
        """Representação da conta bancária."""
        return f"Saldo atual: {self.saldo}"

# Testes
conta = ContaBancaria()

# Realizando alguns depósitos e retiradas
conta.depositar(100, "usuario1")
conta.depositar(200, "usuario2")
conta.retirar(50, "usuario1")
conta.retirar(30, "usuario3")  # Esta tentativa falhará se o saldo for insuficiente

# Exibindo o saldo e o histórico de eventos
print(conta)
print("\nHistórico de Eventos:")
for evento in conta.historico_eventos():
    print(evento)

# Reconstruindo o saldo e o histórico de eventos
print("\nReconstruindo o saldo...")
conta.reconstruir_saldo()
print(conta)
