from django.db import models

# Create your models here.


class Survey(models.Model):
    # a survey has many polls, each poll has many choices 
    survey = models.CharField(max_length = 100)
    pub_date = models.DateField('date created')
    author = models.CharField(max_length = 30)
    popularity = models.IntegerField(default = 0, null=True)
    comment = models.CharField(max_length = 500, null=True )
    # show results properly
    def __unicode__(self):
        return self.survey
class Poll(models.Model):
    # each Poll belongs to a survey
    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    # each choice belongs to a Poll
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length = 100)
    votes = models.IntegerField(default = 0, null=True)
    def __unicode__(self):
        return self.choice
    
    
class VoteRecord(models.Model):
    # the vote record 
    survey = models.ForeignKey(Survey)
    username = models.CharField(max_length = 30)
    comment = models.CharField(max_length = 500, null=True )
    def __unicode__(self):
        return self.username
