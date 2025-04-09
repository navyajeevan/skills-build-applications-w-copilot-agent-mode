from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections using raw MongoDB operations
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear existing data explicitly using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        users = {}
        for user_data in test_data['users']:
            user = User.objects.create(
                email=user_data['email'],
                name=user_data['username']
            )
            users[user.name] = user

        # Populate teams
        for team_data in test_data['teams']:
            team = Team.objects.create(
                name=team_data['name'],
                members=[]  # Initialize members as an empty list
            )
            for member_username in team_data.get('members', []):
                if member_username in users:
                    team.members.append(users[member_username].email)  # Add email addresses only
            team.save()

        # Populate activities
        for activity_data in test_data['activities']:
            Activity.objects.create(
                user=users.get(activity_data['user']),
                type=activity_data['activity_type'],
                duration=int(activity_data['duration'].total_seconds()),  # Convert timedelta to seconds
                date=activity_data['date']
            )

        # Populate leaderboard
        for leaderboard_data in test_data['leaderboard']:
            Leaderboard.objects.create(
                user=users.get(leaderboard_data['user']),
                score=leaderboard_data['score']
            )

        # Populate workouts
        for workout_data in test_data['workouts']:
            Workout.objects.create(
                name=workout_data['name'],
                description=workout_data['description']
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
