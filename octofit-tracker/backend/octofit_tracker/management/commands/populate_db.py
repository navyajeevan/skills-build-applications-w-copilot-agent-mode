from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Drop the users collection in MongoDB to ensure no duplicates exist
        db.users.drop()

        # Debugging: Log the count of documents in the users collection after dropping it
        self.stdout.write(self.style.SUCCESS(f"Users collection count after drop: {db.users.count_documents({})}"))

        # Verify the state of the users collection after dropping it
        if db.users.count_documents({}) > 0:
            self.stdout.write(self.style.ERROR("Failed to drop the users collection. Aborting operation."))
            return

        # Log and handle unexpected duplicates before using get_or_create
        for email in User.objects.values_list('email', flat=True).distinct():
            duplicates = User.objects.filter(email=email)
            if duplicates.count() > 1:
                self.stdout.write(self.style.WARNING(f"Duplicate users found for email {email}. Deleting extras."))
                duplicates.exclude(pk=duplicates.first().pk).delete()

        # Debugging: Log the state of the users collection after each operation
        self.stdout.write(self.style.SUCCESS(f"Users collection count after clearing duplicates: {db.users.count_documents({})}"))

        # Final verification to ensure no duplicates exist before proceeding
        for email in User.objects.values_list('email', flat=True).distinct():
            duplicates = User.objects.filter(email=email)
            if duplicates.count() > 1:
                self.stdout.write(self.style.ERROR(f"Duplicates still exist for email {email}. Aborting operation."))
                return

        # Use get_or_create to ensure each User object is created only once
        users = {
            'thundergod@mhigh.edu': User.objects.get_or_create(email='thundergod@mhigh.edu', defaults={'name': 'thundergod'})[0],
            'metalgeek@mhigh.edu': User.objects.get_or_create(email='metalgeek@mhigh.edu', defaults={'name': 'metalgeek'})[0],
            'zerocool@mhigh.edu': User.objects.get_or_create(email='zerocool@mhigh.edu', defaults={'name': 'zerocool'})[0],
            'crashoverride@mhigh.edu': User.objects.get_or_create(email='crashoverride@mhigh.edu', defaults={'name': 'crashoverride'})[0],
            'sleeptoken@mhigh.edu': User.objects.get_or_create(email='sleeptoken@mhigh.edu', defaults={'name': 'sleeptoken'})[0],
        }

        # Refresh the users list by querying the database for unique email addresses
        users = {user.email: user for user in User.objects.all()}

        # Explicitly save each User object individually to ensure they are fully persisted
        for user in users.values():
            user.save()

        # Debugging: Log the state of users after clearing and repopulating the database
        self.stdout.write(self.style.SUCCESS(f"Users after clearing and repopulating: {[user.email for user in User.objects.all()]}"))

        # Debugging: Log the primary keys of User objects to ensure they are valid
        for email, user in users.items():
            self.stdout.write(self.style.SUCCESS(f"User: {email}, PK: {user.pk}"))

        # Explicitly remove duplicate User entries
        for email in User.objects.values_list('email', flat=True).distinct():
            duplicates = User.objects.filter(email=email)
            if duplicates.count() > 1:
                duplicates.exclude(pk=duplicates.first().pk).delete()

        # Add a stricter check to prevent duplicate User objects
        existing_users = {user.email for user in User.objects.all()}
        for email, user in users.items():
            if email in existing_users:
                self.stdout.write(self.style.ERROR(f"Duplicate user detected for email {email}. Skipping creation."))
                continue

        # Create teams
        team1 = Team(name='Blue Team', members=[user.email for user in users.values()][:3])
        team2 = Team(name='Gold Team', members=[user.email for user in users.values()][3:])
        team1.save()
        team2.save()

        # Ensure users remain a dictionary keyed by email addresses
        users = {user.email: user for user in User.objects.all()}

        # Correctly access User objects from the dictionary for debugging
        self.stdout.write(self.style.SUCCESS(f"Unique users in database: {[user.email for user in users.values()]}"))

        # Refresh the users dictionary to ensure it contains only saved User objects
        users = {user.email: User.objects.get(email=user.email) for user in User.objects.all()}

        # Ensure Activity objects reference User objects directly from the database
        activities = [
            Activity(user=User.objects.filter(email='thundergod@mhigh.edu').first(), type='Cycling', duration=60, date='2025-04-01'),
            Activity(user=User.objects.filter(email='metalgeek@mhigh.edu').first(), type='Crossfit', duration=120, date='2025-04-02'),
            Activity(user=User.objects.filter(email='zerocool@mhigh.edu').first(), type='Running', duration=90, date='2025-04-03'),
            Activity(user=User.objects.filter(email='crashoverride@mhigh.edu').first(), type='Strength', duration=30, date='2025-04-04'),
            Activity(user=User.objects.filter(email='sleeptoken@mhigh.edu').first(), type='Swimming', duration=75, date='2025-04-05'),
        ]

        # Debugging: Log the state of activities before saving
        for activity in activities:
            self.stdout.write(self.style.SUCCESS(f"Preparing to save activity: {activity.type} for user {activity.user.email}"))

        # Debugging: Log the state of the user field in each Activity object before saving
        for activity in activities:
            self.stdout.write(self.style.SUCCESS(f"Activity: {activity.type}, User: {activity.user}, User PK: {activity.user.pk}"))

        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(user=users['thundergod@mhigh.edu'], score=100),
            Leaderboard(user=users['metalgeek@mhigh.edu'], score=90),
            Leaderboard(user=users['zerocool@mhigh.edu'], score=95),
            Leaderboard(user=users['crashoverride@mhigh.edu'], score=85),
            Leaderboard(user=users['sleeptoken@mhigh.edu'], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
