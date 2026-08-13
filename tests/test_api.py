"""
API endpoint tests for Mergington High School Activities API.

All tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the API call being tested
- Assert: Verify results match expectations
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


# Test GET /activities endpoint


def test_get_activities_returns_all_activities(client: TestClient):
    """
    Test that GET /activities returns all available activities.
    
    AAA Pattern:
    - Arrange: No special setup needed; using default test data from fixtures
    - Act: Make GET request to /activities
    - Assert: Verify status 200 and all 9 activities are returned
    """
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_get_activities_contains_required_fields(client: TestClient):
    """
    Test that each activity in the response has all required fields.
    
    AAA Pattern:
    - Arrange: Define required fields
    - Act: Get activities and check first activity
    - Assert: Verify all required fields are present
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert set(activity_data.keys()) >= required_fields, \
            f"Activity '{activity_name}' missing required fields"
        assert isinstance(activity_data["participants"], list), \
            f"Participants for '{activity_name}' should be a list"


def test_get_activities_participants_are_emails(client: TestClient):
    """
    Test that participants are email strings.
    
    AAA Pattern:
    - Arrange: Get activities
    - Act: Check participants in each activity
    - Assert: All participants are email-like strings
    """
    # Arrange & Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str), \
                f"Participant in '{activity_name}' should be string"
            assert "@" in participant, \
                f"Participant '{participant}' should be an email"


# Test GET / redirect


def test_root_redirects_to_static_index(client: TestClient):
    """
    Test that GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: No setup needed
    - Act: Make GET request to root path with follow_redirects=False
    - Assert: Verify 307 redirect status and correct location header
    """
    # Arrange & Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


# Test POST /activities/{activity_name}/signup


def test_signup_adds_participant_successfully(client: TestClient):
    """
    Test successful signup for an activity.
    
    AAA Pattern:
    - Arrange: Define test email and activity
    - Act: POST signup request with new email
    - Assert: Verify 200 status, success message, and participant is added
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_signup_prevents_duplicate_signup(client: TestClient):
    """
    Test that a student cannot sign up twice for the same activity.
    
    AAA Pattern:
    - Arrange: Use an existing participant in Chess Club
    - Act: Attempt to sign up with same email again
    - Assert: Verify 400 status with "already signed up" error
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"].lower()


def test_signup_fails_for_nonexistent_activity(client: TestClient):
    """
    Test that signup fails with 404 when activity does not exist.
    
    AAA Pattern:
    - Arrange: Use a non-existent activity name
    - Act: Attempt to sign up for activity that doesn't exist
    - Assert: Verify 404 status with "Activity not found" error
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()


def test_signup_accepts_valid_email_format(client: TestClient):
    """
    Test that signup accepts various valid email formats.
    
    AAA Pattern:
    - Arrange: Define multiple valid email formats
    - Act: Sign up with each email
    - Assert: All requests succeed with 200 status
    """
    # Arrange
    activity_name = "Programming Class"
    test_emails = [
        "student.name@mergington.edu",
        "s123@mergington.edu",
        "user+tag@mergington.edu",
    ]
    
    # Act & Assert
    for email in test_emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200, \
            f"Failed to sign up with email: {email}"


# Test DELETE /activities/{activity_name}/unregister


def test_unregister_removes_participant_successfully(client: TestClient):
    """
    Test successful unregistration of a participant.
    
    AAA Pattern:
    - Arrange: Use an existing participant in Chess Club
    - Act: DELETE request to unregister
    - Assert: Verify 200 status and success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Existing participant
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert "Unregistered" in result["message"]


def test_unregister_fails_for_non_participant(client: TestClient):
    """
    Test that unregister fails with 400 when student is not signed up.
    
    AAA Pattern:
    - Arrange: Use an email that is NOT a participant
    - Act: Attempt to unregister non-participant
    - Assert: Verify 400 status with error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "noone@mergington.edu"  # Not a participant
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"].lower()


def test_unregister_fails_for_nonexistent_activity(client: TestClient):
    """
    Test that unregister fails with 404 when activity does not exist.
    
    AAA Pattern:
    - Arrange: Use a non-existent activity name
    - Act: Attempt to unregister from activity that doesn't exist
    - Assert: Verify 404 status with "Activity not found" error
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()


def test_signup_and_unregister_integration(client: TestClient):
    """
    Test full lifecycle: signup, verify participant added, then unregister.
    
    AAA Pattern:
    - Arrange: Define test data
    - Act: Sign up a new participant, verify they're added, then unregister
    - Assert: Verify each step succeeds
    """
    # Arrange
    activity_name = "Tennis Club"
    email = "integration@mergington.edu"
    
    # Act - Step 1: Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Act - Step 2: Verify participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity_name]["participants"]
    
    # Act - Step 3: Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert - All steps succeeded
    assert unregister_response.status_code == 200
    
    # Assert - Verify participant was removed
    final_response = client.get("/activities")
    final_activities = final_response.json()
    assert email not in final_activities[activity_name]["participants"]


def test_unregister_followed_by_signup(client: TestClient):
    """
    Test that a student can sign up again after unregistering.
    
    AAA Pattern:
    - Arrange: Use existing participant
    - Act: Unregister, then sign up again
    - Assert: Both operations succeed
    """
    # Arrange
    activity_name = "Art Studio"
    email = "isabella@mergington.edu"  # Existing participant
    
    # Act - Step 1: Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Act - Step 2: Sign up again
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Both succeeded
    assert signup_response.status_code == 200
    
    # Assert - Participant is back in the list
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity_name]["participants"]
