from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

# @router.post('/login')
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):    
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
#     # check passowrd
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

#     # create token
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     # return token
#     return {'access_token': access_token, "token_type": "bearer"}

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # when we use OAuth2PasswordRequestForm:
    # user_credentials = {
    #     "username": "ljkslgj",
    #     "password": "ejhrghd"
    # }
    # and also:
    # we no longer send the credentials in the body like before.
    # if we do, we get an error: missing username and password 
    # Instead it expects those inside form data.
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # check passowrd
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {'access_token': access_token, "token_type": "bearer"}