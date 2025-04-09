from datetime import timedelta

test_data = {
    "users": [
        {"id": 1, "username": "thundergod", "email": "thundergod@mhigh.edu", "password": "thundergodpassword"},
        {"id": 2, "username": "metalgeek", "email": "metalgeek@mhigh.edu", "password": "metalgeekpassword"},
        {"id": 3, "username": "zerocool", "email": "zerocool@mhigh.edu", "password": "zerocoolpassword"},
        {"id": 4, "username": "crashoverride", "email": "crashoverride@hmhigh.edu", "password": "crashoverridepassword"},
        {"id": 5, "username": "sleeptoken", "email": "sleeptoken@mhigh.edu", "password": "sleeptokenpassword"},
    ],
    "teams": [
        {"id": 1, "name": "Blue Team", "members": ["thundergod", "metalgeek"]},
        {"id": 2, "name": "Gold Team", "members": ["zerocool", "crashoverride", "sleeptoken"]},
    ],
    "activities": [
        {"id": 1, "user": "thundergod", "activity_type": "Cycling", "duration": timedelta(hours=1), "date": "2025-04-01"},
        {"id": 2, "user": "metalgeek", "activity_type": "Crossfit", "duration": timedelta(hours=2), "date": "2025-04-02"},
        {"id": 3, "user": "zerocool", "activity_type": "Running", "duration": timedelta(hours=1, minutes=30), "date": "2025-04-03"},
        {"id": 4, "user": "crashoverride", "activity_type": "Strength", "duration": timedelta(minutes=30), "date": "2025-04-04"},
        {"id": 5, "user": "sleeptoken", "activity_type": "Swimming", "duration": timedelta(hours=1, minutes=15), "date": "2025-04-05"},
    ],
    "leaderboard": [
        {"id": 1, "user": "thundergod", "score": 100},
        {"id": 2, "user": "metalgeek", "score": 90},
        {"id": 3, "user": "zerocool", "score": 95},
        {"id": 4, "user": "crashoverride", "score": 85},
        {"id": 5, "user": "sleeptoken", "score": 80},
    ],
    "workouts": [
        {"id": 1, "name": "Cycling Training", "description": "Training for a road cycling event"},
        {"id": 2, "name": "Crossfit", "description": "Training for a crossfit competition"},
        {"id": 3, "name": "Running Training", "description": "Training for a marathon"},
        {"id": 4, "name": "Strength Training", "description": "Training for strength"},
        {"id": 5, "name": "Swimming Training", "description": "Training for a swimming competition"},
    ],
}
