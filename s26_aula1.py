import boto3

# Inicialize o cliente do SQS
try:
    sqs = boto3.client('sqs', region_name='us-east-1')
    print("Cliente SQS inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o cliente SQS: {e}")

# Crie uma fila padrão
try:
    response_standard = sqs.create_queue(
        QueueName='StandardQueue'
    )
    standard_queue_url = response_standard['QueueUrl']
    print(f"Fila padrão criada com sucesso! URL: {standard_queue_url}")
except Exception as e:
    print(f"Erro ao criar a fila padrão: {e}")

# Crie uma fila FIFO
try:
    response_fifo = sqs.create_queue(
        QueueName='FIFOQueue.fifo',
        Attributes={
            'FifoQueue': 'true',
            'ContentBasedDeduplication': 'true'
        }
    )
    fifo_queue_url = response_fifo['QueueUrl']
    print(f"Fila FIFO criada com sucesso! URL: {fifo_queue_url}")
except Exception as e:
    print(f"Erro ao criar a fila FIFO: {e}")