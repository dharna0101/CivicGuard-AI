from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.services.auth_service import create_token, decode_token, get_demo_user_passwords, hash_password, verify_password
from app.services.mock_store import MockStore

router = APIRouter()
store = MockStore()


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    name: str
    role: str
    email: str


@router.post("/register", response_model=Token)
def register(user_data: UserRegister):
    existing = store.get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_id = str(uuid4())
    from app.models import User

    user = User(
        id=user_id,
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role.lower(),
        phone=user_data.phone,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    store.create_user(user)
    token = create_token(user.id, user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        role=user.role,
        email=user.email,
    )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = store.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    demo_passwords = get_demo_user_passwords()
    if credentials.email in demo_passwords:
        if credentials.password != demo_passwords[credentials.email]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    else:
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_token(user.id, user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        role=user.role,
        email=user.email,
    )


@router.get("/verify")
def verify_token(token: str):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        user = store.users.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"valid": True, "user_id": user_id, "role": role, "name": user.name, "email": user.email}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
