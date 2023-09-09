from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from db.dbconfig import get_db
from db.utils.auth_utils import check_session, get_user_by_session


async def verify_session(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")

    if not session_id or not check_session(session_id=session_id, db=db):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = get_user_by_session(session_id=session_id, db=db)

    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user
