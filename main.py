import datetime

import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError


app = FastAPI()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Vinogradov_Konstantin:12345@77.91.86.135/isp_p_Vinogradov_Konstantin"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    type = Column(String(50), index=True)
    name = Column(String(100), index=True)

class ProductModel(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(30), index=True)
    product_id = Column(Integer, ForeignKey('product.id'), index=True, nullable=False)
    price = Column(Integer, index=True)

class Entrance(Base):
    __tablename__ = "entrance"

    id = Column(Integer, primary_key=True, index=True)
    product_model_id = Column(Integer, ForeignKey('model.id'), index=True, nullable=False)
    date_entrance = Column(Date, index=True, nullable=False)
    count = Column(Integer, index=True)
    taker = Column(String(100), index=True)
    
Base.metadata.create_all(bind=engine)

class ProductCreate(BaseModel):
    name: str
    type: str

class ProductResponse(BaseModel):
    id: int
    type: str
    name: str

    class Config:
        from_attributes = True

class ProductModelCreate(BaseModel):
    name: str
    product_id: int
    price: int

class ProductModelResponse(BaseModel):
    id: int
    name: str
    product_id: int
    price: int

    class Config:
        from_attributes = True

class EntranceCreate(BaseModel):
    product_model_id: int
    date_entrance: datetime.date
    count: int
    taker: str

class EntranceResponse(BaseModel):
    id: int
    product_model_id: int
    date_entrance: datetime.date
    count: int
    taker: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/product/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="product not found")
    return item

# Маршрут для создания нового пользователя
@app.post("/product/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    item = Product(name=product.name, type=product.type)
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="product was not created")
    


@app.get("/product-model/{product_model_id}", response_model=ProductModelResponse)
def read_product(product_model_id: int, db: Session = Depends(get_db)):
    item = db.query(ProductModel).filter(ProductModel.id == product_model_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="model not found")
    return item

# Маршрут для создания нового пользователя
@app.post("/product-model/", response_model=ProductModelResponse)
def create_product(model: ProductModelCreate, db: Session = Depends(get_db)):
    item = ProductModel(name=model.name, product_id=model.product_id, price=model.price)
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="model was not created")
    

@app.get("/entrance/{entrance_id}", response_model=EntranceResponse)
def read_product(entrance_id: int, db: Session = Depends(get_db)):
    item = db.query(Entrance).filter(Entrance.id == entrance_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="model not found")
    return item

# Маршрут для создания нового пользователя
@app.post("/entrance/", response_model=EntranceResponse)
def create_product(entrance: EntranceCreate, db: Session = Depends(get_db)):
    item = Entrance(product_model_id = entrance.product_model_id, date_entrance = entrance.date_entrance, count=entrance.count, taker = entrance.taker)
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="model was not created")
    