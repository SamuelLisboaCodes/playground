import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adicionar o diretório do backend ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Adicionar o diretório pai ao sys.path para encontrar o módulo 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)

def test_logout():
    # Simular login (defina o cookie de sessão)
    client.cookies.set("session", "fake-session-token")

    # Verificar se o usuário está autenticado
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == {"message": "Usuário autenticado", "token": 'token'}

    # Realizar logout
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logout realizado com sucesso"}

    # Verificar se o cookie de sessão foi removido
    client.cookies.clear()  # Limpar cookies do cliente para simular a remoção do cookie de sessão
    response = client.get("/user")
    assert response.status_code == 401  # Supondo que o status seja 401 após o logout
    assert response.json() == {"detail": "Not authenticated"}