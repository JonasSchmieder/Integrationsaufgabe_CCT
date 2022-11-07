from pydantic import BaseModel

class Candidate(BaseModel):
    uuid: str
    name: str
