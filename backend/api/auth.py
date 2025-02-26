from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from dotenv import load_dotenv
import os
from fastapi.responses import RedirectResponse

import requests
from api.storage import users_collection
load_dotenv()
router = APIRouter()


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"



@router.get("/login")
async def login_com_google():
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={os.getenv("GOOGLE_CLIENT_ID")}&redirect_uri={os.getenv("GOOGLE_REDIRECT_URI")}&response_type=code&scope=openid email profile"
    print(google_auth_url)
    return RedirectResponse(url=google_auth_url)

@router.get("/callback")
async def auth_callback(code: str, request: Request):
    # Trocar o código de autorização pelo token de acesso
    token_data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    tokens = response.json()
    access_token = tokens["access_token"] 
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing id_token in response.")

    try:
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        result = requests.get(user_info_url, headers=headers)
        user_info = result.json()
        
        if not await users_collection.get_user(user_info["id"]):
           created = await users_collection.create_user(user_info["id"], user_info["email"])

        
        await users_collection.update_user_token(user_info["id"], access_token)
        
        # Armazena o email do usuário na sessão
        request.session["user_email"] = user_info["email"]
        
        # edireciona para o frontend com sessão ativa
        response = RedirectResponse(url=f"http://localhost:8501/?email={user_info['email']}")
        response.set_cookie(key="session", value=user_info["email"], httponly=True, secure=False)

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")

@router.get("/session-user")
async def get_session_user(request: Request):
    """Retorna o email do usuário armazenado no Cookie de Sessão."""
    print("session-user" + str(request.session))
    user_email = request.cookies.get("session")
    print(user_email)
    if not user_email:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")
    return {"email": user_email}

@router.get("/logout")
async def logout(response: Response):
    """Remove a sessão do usuário apagando o Cookie."""
    response = RedirectResponse(url="http://localhost:8501")
    response.delete_cookie("session_id")
    return response

@router.post("/refresh")
async def refresh_token_endpoint(user_id: str):
    """Atualiza o access token usando o refresh token armazenado no banco."""

    user = await users_collection.get_user(user_id)

    if not user or "refresh_token" not in user:
        raise HTTPException(status_code=400, detail="Refresh token não encontrado.")

    new_access_token = refresh_access_token(user["refresh_token"])

    await users_collection.update_user_token(user_id, user["refresh_token"])

    return {"access_token": new_access_token}

def refresh_access_token(refresh_token: str) -> dict:
    """Troca um refresh token por um novo access token"""
    
    token_data = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data).json()

    if "access_token" not in token_response:
        raise HTTPException(status_code=400, detail="Erro ao renovar token de acesso")

    return {
        "access_token": token_response["access_token"],
        "refresh_token": token_response.get("refresh_token", refresh_token),  # Atualiza se um novo for gerado
    }
