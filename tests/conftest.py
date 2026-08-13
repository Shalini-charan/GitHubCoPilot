"""
Pytest configuration and shared fixtures for API tests.

This module provides:
- TestClient: FastAPI test client for making synchronous API calls
- override_activities: Fixture that provides fresh, isolated activities data per test
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as default_activities


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient for making API calls in tests.
    
    The client is set up to use the app with its current configuration.
    """
    return TestClient(app)


@pytest.fixture
def override_activities():
    """
    Provide a fresh copy of activities data for each test.
    
    This fixture:
    - Creates a deep copy of the default activities
    - Ensures test isolation (changes in one test don't affect others)
    - Allows tests to modify the data without side effects
    
    Yields:
        dict: A fresh copy of the activities dictionary with sample data
    """
    # Create a fresh copy of activities with the same structure
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Join our school band and perform at events",
            "schedule": "Mondays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["mason@mergington.edu", "chloe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM concepts",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    yield test_activities
