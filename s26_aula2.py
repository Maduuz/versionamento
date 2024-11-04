import boto3
from botocore.exceptions import ClientError

# Inicialize o cliente do SQS e KMS
try:
    sqs = boto3.client('sqs', region_name='us-east-1')
    print("Cliente SQS inicializado com sucesso!")
except ClientError as e:
    print(f"Erro ao inicializar o cliente SQS: {e}")

try:
    kms = boto3.client('kms', region_name='us-east-1')
    print("Cliente KMS inicializado com sucesso!")
except ClientError as e:
    print(f"Erro ao inicializar o cliente KMS: {e}")

# Crie uma chave no KMS para uso com a fila do SQS
try:
    response_kms = kms.create_key(
        Description='Chave KMS para criptografia do SQS'
    )
    key_id = response_kms['KeyMetadata']['KeyId']
    print(f"Chave KMS criada com sucesso! ID: {key_id}")
except ClientError as e:
    print(f"Erro ao criar chave KMS: {e}")
    print(e.response['Error']['Message'])
    key_id = None
except Exception as e:
    print(f"Erro inesperado: {e}")
    key_id = None

# Crie uma fila SQS com criptografia se a chave KMS foi criada com sucesso
if key_id:
    try:
        response_sqs = sqs.create_queue(
            QueueName='SecureQueue',
            Attributes={
                'KmsMasterKeyId': key_id
            }
        )
        queue_url = response_sqs['QueueUrl']
        print(f"Fila SQS criada com sucesso! URL: {queue_url}")
    except ClientError as e:
        print(f"Erro ao criar fila SQS: {e}")
        print(e.response['Error']['Message'])
        queue_url = None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        queue_url = None
else:
    queue_url = None
    print("Não foi possível criar a fila SQS porque a chave KMS não foi criada com sucesso.")

# Enviando uma mensagem criptografada para a fila se a fila foi criada com sucesso
if queue_url:
    try:
        response_send = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody='Mensagem criptografada de teste',
            MessageAttributes={
                'AttributeOne': {
                    'StringValue': 'Valor do Atributo',
                    'DataType': 'String'
                }
            }
        )
        print("Mensagem enviada com sucesso!")
    except ClientError as e:
        print(f"Erro ao enviar mensagem: {e}")
        print(e.response['Error']['Message'])
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Recebendo a mensagem criptografada da fila se a fila foi criada com sucesso
if queue_url:
    try:
        response_receive = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
            MessageAttributeNames=['All']
        )
        if 'Messages' in response_receive:
            for message in response_receive['Messages']:
                print(f"Mensagem recebida: {message['Body']}")
                # Apaga a mensagem após o processamento
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print("Nenhuma mensagem recebida.")
    except ClientError as e:
        print(f"Erro ao receber mensagem: {e}")
        print(e.response['Error']['Message'])
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Apague a fila e a chave do KMS para limpeza se a fila e a chave foram criadas com sucesso
if queue_url:
    try:
        sqs.delete_queue(QueueUrl=queue_url)
        print("Fila SQS apagada com sucesso!")
    except ClientError as e:
        print(f"Erro ao apagar fila SQS: {e}")
        print(e.response['Error']['Message'])
    except Exception as e:
        print(f"Erro inesperado: {e}")

if key_id:
    try:
        kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
        print("Chave KMS agendada para exclusão.")
    except ClientError as e:
        print(f"Erro ao agendar exclusão da chave KMS: {e}")
        print(e.response['Error']['Message'])
    except Exception as e:
        print(f"Erro inesperado: {e}")

