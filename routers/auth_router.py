from typing import Annotated, Optional

from fastapi import APIRouter, status, Depends, Response, Request, Cookie, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import dotenv_values

from middleware.verify_session import verify_session
from db.utils.auth_utils import (
    get_user,
    authenticate_user,
    add_user,
    create_session,
    check_session,
    delete_session,
    pwd_context,
)
from db.dbconfig import get_db
from schemas.user import User, UserInDB

enviroment_variables = dotenv_values(".env")


router = APIRouter(prefix="/auth", tags=["Base endpoint to authenticate users"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incorrect username or password",
        )

    session = create_session(db=db, user=user)
    response.set_cookie(
        key="session_id", value=session.session_id, samesite="lax", httponly=True  # type: ignore
    )

    return user


@router.get("/session", status_code=status.HTTP_200_OK)
async def check_user_session(
    session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
    )
    if not session_id:
        raise exception

    authenticated = check_session(db=db, session_id=session_id)

    if not authenticated:
        raise exception

    return True


@router.delete("/session", status_code=status.HTTP_200_OK)
async def logout_user(
    response: Response,
    session_id: Optional[str] = Cookie(None),
    db: Session = Depends(get_db),
):
    if not session_id:
        return True

    response.delete_cookie(key="session_id")
    delete_session(db=db, session_id=session_id)

    return True


# @router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
# async def register_user(user: UserInDB, db: Session = Depends(get_db)):
#     user_existing = get_user(db=db, username=user.username)
#     if user_existing:
#         raise HTTPException(
#             status.HTTP_406_NOT_ACCEPTABLE, detail="Username already exists."
#         )

#     hashed_password = pwd_context.hash(user.password)
#     old_user = user.model_dump(exclude="password")

#     hashed_user = UserInDB(password=hashed_password, **old_user)

#     user = add_user(user=hashed_user, db=db)

#     return user


@router.get("/user", response_model=User)
async def read_users_me(user: User = Depends(verify_session)):
    return user
