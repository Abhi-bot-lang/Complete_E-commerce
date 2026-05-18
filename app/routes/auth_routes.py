from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import User_Schema, LoginSchema
from app.models.user_model import User
from app.config.database import get_db
from app.utils.hash_password import hash_password, verify_password
from app.utils.JWT import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/register")
def register(user: User_Schema, db: Session = Depends(get_db)):

    # Check existing user
    existing_user = db.query(User).filter(User.Email == user.Email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    hashed_password = hash_password(user.Password)

    # Create user
    db_user = User(
        FirstName=user.FirstName,
        LastName=user.LastName,
        Email=user.Email,
        Password=hashed_password,
        Role=user.Role
    )

    # Save user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User Registered Successfully",
        "data": {
            "id": db_user.id,
            "Email": db_user.Email,
            "Role": db_user.Role
        }
    }


@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):

    # Find user
    db_user = db.query(User).filter(User.Email == user.Email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify password
    if not verify_password(user.Password, db_user.Password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    # Generate tokens
    access_token = create_access_token({"sub": db_user.Email})
    refresh_token = create_refresh_token({"sub": db_user.Email})

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }