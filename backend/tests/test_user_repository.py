
import pytest
import asyncio
from datetime import datetime

from ..config.models import User


@pytest.fixture
def test_sample_user():
    """Retorna um usuário de teste."""
    return User(
        id="user_001",
        email="user@example.com",
        refresh_token=None,
        created_at=datetime.now(),
        assistants=[]
    )
