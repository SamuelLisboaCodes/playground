from fastapi import APIRouter, Depends, HTTPException, Request, status
from dotenv import load_dotenv
import os
from fastapi.responses import RedirectResponse
import httpx
from pymongo import MongoClient
import requests
from backend.config.repositories.user_repository import MongoUserRepository
from google.oauth2 import id_token
from api.storage import mongo_db_client
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
        response = requests.get(user_info_url, headers=headers)
        user_info = response.json()
        user_db = MongoUserRepository(mongo_db_client)
        print(user_info["id"])
        if not await user_db.get_user(user_info["id"]):
           created = await user_db.create_user(user_info["id"], user_info["email"])
        updated_user = await user_db.update_user_token(user_info["id"], tokens["access_token"])
        print(updated_user)
        
        redirect_url = f"http://localhost:8501?token={tokens["id_token"]}"
        return RedirectResponse(url=redirect_url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")


def refresh_access_token(refresh_token: str) -> str:
    token_data = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data).json()

    if "access_token" not in token_response:
        raise HTTPException(status_code=400, detail="Erro ao renovar token de acesso")

    return token_response["access_token"]