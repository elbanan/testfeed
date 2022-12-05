from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    medabbr = models.CharField(max_length=100)
    radiology = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name


class Article(models.Model):
    pmid = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    abstract = models.CharField(max_length=1000)
    url = models.CharField(max_length=100)
    pubdate = models.DateField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.pmid)


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    WEEK_DAYS = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ManyToManyField(Journal)
    frequency = models.IntegerField(default=1)
    day_of_week = models.IntegerField(default=1, choices=WEEK_DAYS)
    bookmarks = models.ManyToManyField(Article)
    keywords = models.CharField(max_length=1000, null=True)
    # upvotes = models.ManyToManyField(Article)
    # downvotes = models.ManyToManyField(Article)

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)