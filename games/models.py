from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
    date = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=5)
    is_solved = models.BooleanField(default=False)
    total_attempts = models.IntegerField(default=0)

    def __str__(self):
	    return f"{self.user.username} - {self.date} - {'Solved' if self.is_solved else 'Unsolved'}"


class Guess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guesses')
    date = models.DateField(auto_now_add=True)
    guess_word = models.CharField(max_length=5)
    result = models.CharField(max_length=5)
    attempt_times = models.IntegerField(default=1)

    def __str__(self):
    	return f"{self.user.username} guessed {self.guess_word} ({self.result})"

    class Meta:
        indexes = [models.Index(fields=["date"])]