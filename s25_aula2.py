import random

class Queue:
    def __init__(self):
        self.messages = []

    def enqueue(self, message):
        self.messages.append(message)

    def dequeue(self):
        if self.messages:
            return self.messages.pop(0)
        return None

# Fila principal e DLQ
main_queue = Queue()
dlq = Queue()

def deliver_message(message):
    # Simular falha aleatória para testes
    if random.choice([True, False]):
        raise Exception("Erro de entrega.")

def process_message(message, max_attempts):
    attempts = message.get('attempts', 0)

    try:
        # Tente entregar a mensagem
        deliver_message(message)
        print(f"Mensagem '{message['content']}' entregue com sucesso.")
    except Exception as e:
        print(f"Falha ao entregar a mensagem: {e}")
        attempts += 1
        
        if attempts < max_attempts:
            message['attempts'] = attempts
            main_queue.enqueue(message)  # Reenfileira a mensagem
            print(f"Mensagem reenfileirada. Tentativa {attempts}.")
        else:
            dlq.enqueue(message)  # Move para a DLQ
            print(f"Mensagem movida para a DLQ após {attempts} tentativas.")

# Simulando mensagens
for i in range(5):
    main_queue.enqueue({'content': f'Mensagem {i + 1}', 'attempts': 0})

# Processando mensagens
while main_queue.messages:
    msg = main_queue.dequeue()
    process_message(msg, max_attempts=3)

# Monitoramento da DLQ
print("\nMensagens na DLQ:")
for message in dlq.messages:
    print(f"- {message['content']} (Tentativas: {message['attempts']})")
