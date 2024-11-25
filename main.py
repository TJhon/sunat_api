from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select

from api.database import engine
from api.cotizations import (
    Cotization,
    CotizationBase,
    CotizationResult,
    CotizationResultBase,
)
from src.Information import Info


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def add_to_db(table: SQLModel, to_add, db: Session):
    to_add = table.model_validate(to_add)
    db.add(to_add)
    db.commit()
    db.refresh(to_add)
    return to_add


depend = Depends(get_session)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"hola mundo"}


@app.get("/user_cotization/{username}")
def get_user_cotization(*, db: Session = depend, username: str):
    table = CotizationResult
    query = select(table).where(table.user == username)
    result = db.exec(query).all()
    return result


@app.get("/user_cotizacion/{username}_{hscode}")
def get_hs_cotization(*, db: Session = depend, username: str, hscode: str):
    table_values = Cotization
    table_result = CotizationResult
    query = select(table_result).where(
        table_result.user == username, table_result.hscode == hscode
    )
    result = db.exec(query).first()
    return result


@app.post("/cotization_values/")
def create_cotization(*, db: Session = depend, inputs: CotizationBase):
    exists = get_hs_cotization(db=db, username=inputs.user, hscode=inputs.hscode)
    if exists:
        return exists
    data = add_to_db(Cotization, inputs, db)
    return data


@app.patch("/cotization_result/{username}_{hscode}")
def update_user_item(*, username: str, hscode: str):
    db = CotizationResult
    item = get_user_cotization(db=db, username=username, hscode=hscode)
    print("updated")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
    # item_data


@app.post("/cotization_result/")
def create_result_cotization(*, db: Session = depend, result: CotizationResultBase):
    item_exists = get_hs_cotization(db=db, username=result.user, hscode=result.hscode)
    if item_exists:
        return item_exists
    data = add_to_db(CotizationResult, result, db)
    return data


@app.delete("/cotization_result/{username}_{hscode}")
def delete_hs(*, db: Session = depend, username: str, hscode: str):
    item = get_hs_cotization(db=db, username=username, hscode=hscode)
    if not item:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(item)
    db.commit()
    return {"ok": True}
