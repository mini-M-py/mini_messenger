from fastapi import status, HTTPException, APIRouter, Depends

from .. import model,schemas
from sqlalchemy.orm import Session

from .. database import get_db, engine

router = APIRouter()
 


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.user_out)
def create_user(user: schemas.create_user, db:Session = Depends(get_db)):
    #checking email on database
    email_query = db.query(model.User).filter(model.User.email == user.email)
    email_found = email_query.first()
    
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with email already exist")
    else:
        user.dict()
        print(user)
        new_user =model.User(user_name = user.user_name, email = user.email, password = user.password)
        db.add(new_user)
        db.commit()
        #db.refersh(new_user)

        return new_user