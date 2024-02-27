from typing import List, Optional
from fastapi import Response, status, HTTPException, APIRouter, Depends

from .. import model,schemas, utils, email, oauth2
from sqlalchemy.orm import Session

from .. database import get_db, engine

router = APIRouter(
    tags=["User"],
    prefix="/users"
    )
 


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.user_out)
def create_user(user: schemas.create_user, db:Session = Depends(get_db)):
    #checking email on database
    email_query = db.query(model.User).filter(model.User.email == user.email)
    email_found = email_query.first()
    
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with email already exist")
    else:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        user.dict()
        
        #verifing otp
        if not utils.verify_otp(user.email, user.otp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        new_user =model.User(user_name = user.user_name, email = user.email, password = user.password)
        db.add(new_user)
        db.commit()
        #db.refersh(new_user)

        return new_user
    

@router.post("/verify",status_code=status.HTTP_202_ACCEPTED)
def verify(user: schemas.verify,db: Session = Depends(get_db)):
    otp = utils.generate_otp()
    email.send_email(user.email, otp)
    utils.save_otp(user.email, otp)
    return {"message":"otp has been sent to your email."}

@router.delete('/')
def delete_user(user: schemas.delete_user, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    current_user = int(user_id.id)
    #seraching user on database

    user_query = db.query(model.User).filter(model.User.id == current_user)
    user_found = user_query.first()

    if user_found == None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"server busy!!, Please relogin")
    
    #verifying password
    if not utils.verify(user_found.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'InvalidCredential')
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/')
def get_user( db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),search: Optional[str] = ""):
    users = db.query(model.User).filter(model.User.user_name.contains(search)).all()

    enc_user = []
    for user in users:
        enc_id = utils.encrypt(user.id)
        uniqueId = utils.uniqueId(user.id)

        enc_user.append({"id": enc_id,"uniqueId": uniqueId, "user_name": user.user_name})

    return enc_user
