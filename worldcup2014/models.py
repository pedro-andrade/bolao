from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
            
class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return self.name
        
class Match(models.Model):
    teamA = models.ForeignKey(Team, related_name='teamA')
    teamB = models.ForeignKey(Team, related_name='teamB')
    matchtime = models.DateTimeField('Date')
    striker = models.CharField(max_length=200)
    winner = models.CharField(max_length=200)
    score = models.CharField(max_length=200)

class Bet(models.Model):
    userid = models.ForeignKey(User)
    matchid = models.ForeignKey(Match)
    striker = models.CharField(max_length=200)
    winner = models.CharField(max_length=200)
    score = models.CharField(max_length=200)
