from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session as DBSession
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from db.models import UserORM, SessionORM
from schemas.user import UserInDB, User
from schemas.session import Session


oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
enviroment_variables = dotenv_values(".env")

# *******************************************************************************************
#
#                               START OF AUTH UTILITIES
#
# *******************************************************************************************


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: DBSession, username: str):
    user = db.query(UserORM).filter_by(username=username).first()
    if user:
        return UserInDB(**user.to_dict())


def add_user(db: DBSession, user: UserInDB) -> User:
    # La función recibe user, que es del tipo UserInDB (schema de pydantic) y devuelve un User (schema de pydantic)

    added_user = UserORM(**user.model_dump())
    # Se convierte el usuario de pydantic a una instancia de UserORM (modelo de sqlalchemy)

    db.add(added_user)
    db.commit()
    # Y se agrega a la base de datos

    parsedUser = added_user.to_dict()
    # Posteriormente se hace la reconversión a un modelo de pydantic sin la password

    return User(**parsedUser)


def authenticate_user(db: DBSession, username: str, password: str):
    users = db.query(UserORM).all()

    for user in users:
        print(user.username)
        print("^ user")

    user = get_user(db=db, username=username)

    if not user:
        return False

    # if not verify_password(password, user.password):
    #     return False

    user = User(**user.model_dump())

    return user


def get_all(db: DBSession):
    return db.query(User).all()


def get_user_by_session(db: DBSession, session_id: str):
    try:
        session = db.query(SessionORM).filter_by(session_id=session_id).first()
    except:
        return

    if session:
        user = db.query(UserORM).filter_by(id=session.user_id).first()

        if user:
            return User(**user.to_dict())


# *******************************************************************************************
#
#                                   END OF AUTH UTILITIES
#
# *******************************************************************************************


# *******************************************************************************************
#
#                               START OF SESSION UTILITIES
#
# *******************************************************************************************


def check_session(db: DBSession, session_id: str) -> bool:
    session = db.query(SessionORM).filter_by(session_id=session_id)

    if session:
        return True

    return False


def create_session(db: DBSession, user: User) -> Session:
    exists_session_for_user = check_session_by_user(db=db, user_id=user.id)

    if exists_session_for_user:
        delete_session(db=db, session_id=exists_session_for_user.session_id)  # type: ignore

    expiration = str(datetime.now() + timedelta(days=30))
    created_at = str(datetime.now())
    session = SessionORM(expiration_at=expiration.__str__(), user_id=user.id)

    db.add(session)
    db.commit()

    parsed_session = Session(
        created_at=created_at,
        expiration_at=expiration,
        session_id=session.session_id,  # type: ignore
        user_id=user.id,
    )

    return parsed_session


def delete_session(db: DBSession, session_id: str) -> bool:
    session = db.query(SessionORM).filter_by(session_id=session_id).first()

    if session:
        db.delete(session)
        db.commit()
        return True
    return False


def check_session_by_user(db: DBSession, user_id: int) -> Optional[SessionORM]:
    session = db.query(SessionORM).filter_by(user_id=user_id).first()
    if session:
        return session
