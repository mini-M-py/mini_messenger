from fastapi import status, HTTPException, APIRouter, Depends

from .. import model,schemas, utils, email
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