from pydantic import BaseModel


class LeadCreate(BaseModel):
    name: str
    email: str
    company: str | None = None
    message: str | None = None


class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    company: str | None
    message: str | None
    score: int
    status: str

    class Config:
        from_attributes = True
