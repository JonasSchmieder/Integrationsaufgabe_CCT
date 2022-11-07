from fastapi import FastAPI,HTTPException

from models.candidate_model import Candidate
from models.vote_model import Vote


app = FastAPI()

candidates = []
candidates_uuids = []
voted = []
votes = {}


@app.post("/apiv1/create_candidate/")
async def create_candidate(candidate: Candidate) -> Candidate:
    if candidate in candidates:
        raise HTTPException(status_code=409, detail=f'Candidate with uuid {candidate.uuid} already exists')
    candidates.append(candidate)
    candidates_uuids.append(candidate.uuid)
    return candidate


@app.get("/apiv1/candidates_list/")
async def list_candidates() -> list[Candidate]:
    return candidates

@app.post("/apiv1/vote/")
async def vote(vote:Vote) -> Vote:
    candidate = vote.candidate_uuid
    voter = vote.voter_uuid
    if voter in voted:
        raise HTTPException(status_code=405, detail=f'Voter with uuid {voter } already voted')
    if candidate not in candidates_uuids:
        raise HTTPException(status_code=409, detail=f'Candidate with uuid {candidate} doesnt exists')
    voted.append(voter)
    if candidate in votes.keys():
        votes[candidate] += 1
    else:
        votes[candidate] = 1
    return vote

@app.get("/apiv1/current_winner/")
async def current_winner() -> list[Candidate]:
    if votes:
        winner_uuids = []
        first_winner = max(votes)
        winner_uuids.append(first_winner)
        for voting in votes:
            if votes[voting] == votes[first_winner] and not voting == first_winner:
                winner_uuids.append(voting)
        winners = [candidate for candidate in candidates if candidate.uuid in winner_uuids]
        return winners
    else:
        raise HTTPException(status_code=409, detail=f'No Votes')
