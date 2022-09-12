from xmlrpc.client import boolean
from fastapi import FastAPI
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# ----- /tomatoTest ------ #
@app.post("/jwt")
def test():
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.gdvwkiNW_Il_XZq-ZxsuM7bczINyBzJX18-A95jrr_6sxyQmJnpe5s3UGqukB2oyRFM-r87VSUh5nsNLAblDXPx2qzD70Mu87BSIxDKnUejAuyXRUZHtM-Nb7pZNU4rULB47bQqT2ATbO8BQdHgJCqSBr1agMOzLCdwRUh0JPzqvcZrnsGP1-T3BrYDm_Kf-p7wYvkgPGIXfWgbjHvBqWiuLyH9gkK8AhGemfZwQgitiDuk6ylJlYcGLy2z8xhD13or7ZyaaEoh_3EdOki1_RDZIvdqp1uwcycF5Bp0dDdsMwtn3JvvLcUG10mlsJrOElLd_nr0zd_YY5wFXFY1b0w"
    return {"token":token}


# ----- /user ------ #

@app.post("/user/check", response_model={})
def check_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        return {"isUserSignnedUp": False}
    return {"isUserSignnedUp": True}


@app.post("/user/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered. このメールアドレスは登録されています。")
    return crud.create_user(db=db, user=user)


@app.post("/user/login", response_model=schemas.User)
def create_user(user: schemas.UserVerify, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email has not been registered. このメールアドレスは登録されていません。")

    isLoginSuccess = crud.verify_password(user.password, db_user.hashed_password)
    if not isLoginSuccess:
        raise HTTPException(status_code=400, detail="Email not matches password. メールアドレスとパスワードがマッチしません。")
    
    return db_user

if __name__ == '__main__':
    uvicorn.run(app=app)
