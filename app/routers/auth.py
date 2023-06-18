from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import model, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=['login'])


@router.post('/login' ,response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'InvalidCredential')

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'InvalidCredential')
    access_token = oauth2.create_access_token(data= {'user_id': user.id})
    return{'access_token':access_token, 'token_type': 'bearer'}

@router.put("/forget",  response_model=schemas.user_out)
def forget( user: schemas.forget_password,db:Session = Depends(get_db)):
    #checking email on database
    user_query = db.query(model.User).filter(model.User.email == user.email)
    user_found = user_query.first()
    
    if user_found is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with email does not exist")
    else:
        hashed_password = utils.hash(user.new_password)
        user.new_password = hashed_password
        user.dict()
        
        #verifing otp
        if not utils.verify_otp(user.email, user.otp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
      
        user_found.password = hashed_password
        db.commit()
        #db.refersh(new_user)

        return user_found