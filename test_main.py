from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_candidates_empty():
    response = client.get("/apiv1/candidates_list/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_candidate():
    response = client.post(
        "/apiv1/create_candidate/",
        json={
            "uuid": "test",
            "name": "test"
            }
        )
    assert response.status_code == 200
    assert response.json() == {
            "uuid":"test",
            "name":"test"
            }

def test_create_candidate_duplicate():
    client.post(
        "/apiv1/create_candidate/",
        json={
            "uuid": "test",
            "name": "test"
            }
        )
    response = client.post(
        "/apiv1/create_candidate/",
        json={
            "uuid": "test",
            "name": "test"
        }
    )
    assert response.status_code == 409
    assert response.json() == {
            "detail":'Candidate with uuid test already exists'
            }

def test_list_candidates_singe():
    response = client.get("/apiv1/candidates_list/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "uuid":"test",
            "name":"test"
            }
    ]

def test_list_candidates():
    client.post(
        "/apiv1/create_candidate/",
        json={
            "uuid": "test2",
            "name": "test2"
        }
    )
    client.post(
        "/apiv1/create_candidate/",
        json={
            "uuid": "test3",
            "name": "test3"
        }
    )
    response = client.get("/apiv1/candidates_list/")
    assert response.status_code == 200
    assert response.json() == [{
        "uuid": "test",
        "name": "test"
    },
    {
        "uuid": "test2",
        "name": "test2"
    },
    {
        "uuid": "test3",
        "name": "test3"
    }
    ]

def test_vote_fail():
    response = client.post("/apiv1/vote/",json={
            "voter_uuid": "voter1",
            "candidate_uuid": "test5"
        })
    assert response.status_code == 409
    assert response.json() == {"detail":'Candidate with uuid test5 doesnt exists'}

def test_current_winner_empty():
    response =client.get("/apiv1/current_winner/")
    assert response.status_code == 409
    assert response.json() == {"detail": 'No Votes'}

def test_vote():
    response = client.post("/apiv1/vote/",json={
            "voter_uuid": "voter1",
            "candidate_uuid": "test"
        })
    assert response.status_code == 200
    assert response.json() == {
            "voter_uuid": "voter1",
            "candidate_uuid": "test"
        }

def test_current_winner():
    response =client.get("/apiv1/current_winner/")
    assert response.status_code == 200
    assert response.json() == [{
            "uuid": "test",
            "name": "test"
            }]