from djongo import models

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set AutoField for primary key
    email = models.EmailField(unique=True)  # Ensure email is unique
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Team(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set AutoField for primary key
    name = models.CharField(max_length=255)
    members = models.JSONField()

    def __str__(self):
        return self.name

class Activity(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set AutoField for primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    duration = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.user.email}"

class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set AutoField for primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.email} - {self.score}"

class Workout(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set AutoField for primary key
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
