from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: str
    courier_id: str | None = None
    status: str
    description: str | None = None


class OrderCreate(OrderBase):
    """
    Data needed to create a new order.
    Right now this is the same as `OrderBase`.
    """

    pass


class OrderRead(OrderBase):
    id: str

    class Config:
        from_attributes = True

