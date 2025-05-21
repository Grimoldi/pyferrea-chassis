from pydantic import BaseModel


class FerreaError(BaseModel):
    uuid: str
    code: str
    title: str
    message: str
