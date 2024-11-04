import jwt
import datetime

# Chave secreta para assinar os tokens
SECRET_KEY = "sua_chave_secreta"

def gerar_token(user_id, secret_key, expiration_minutes):
    # Cria a carga útil do token
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }
    # Gera o token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validar_token(received_token, secret_key):
    try:
        # Decodifica o token
        payload = jwt.decode(received_token, secret_key, algorithms=['HS256'])
        # Verifica se o token é válido e extrai o user_id
        user_id = payload['user_id']
        return {"valid": True, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "message": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"valid": False, "message": "Token inválido"}

# Exemplo de uso

# Geração do token para o usuário com id 123
token = gerar_token(123, SECRET_KEY, 30)
print(f"Token gerado: {token}")

# Validação do token
resultado = validar_token(token, SECRET_KEY)
if resultado['valid']:
    print(f"Token válido para o user_id: {resultado['user_id']}")
else:
    print(f"Erro: {resultado['message']}")

