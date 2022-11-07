from pydantic import BaseModel

class Vote(BaseModel):
    voter_uuid: str
    candidate_uuid: str
