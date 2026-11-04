import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def isolated_activity():
    activity_name = "Chess Club"
    participants = activities[activity_name]["participants"]
    original_participants = participants.copy()
    participants.clear()

    try:
        yield activity_name
    finally:
        participants[:] = original_participants


def test_signup_adds_participant(client, isolated_activity):
    email = "student@example.com"

    response = client.post(
        f"/activities/{isolated_activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in activities[isolated_activity]["participants"]


def test_signup_rejects_duplicate_participant(client, isolated_activity):
    email = "student@example.com"
    endpoint = f"/activities/{isolated_activity}/signup"

    first_response = client.post(endpoint, params={"email": email})
    duplicate_response = client.post(endpoint, params={"email": email})

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert activities[isolated_activity]["participants"].count(email) == 1


def test_unregister_removes_participant(client, isolated_activity):
    email = "student@example.com"
    activities[isolated_activity]["participants"].append(email)

    response = client.delete(
        f"/activities/{isolated_activity}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[isolated_activity]["participants"]