from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    item: str
    amount: float

class InvoiceOut(BaseModel):
    id: int
    item: str
    amount: float

    class Config:
        orm_mode = True
