'''
Created on Dec 15, 2011

@author: roy
'''
from models import  Survey
from models import  Poll
from models import  Choice
from models import VoteRecord
from django.contrib import  admin


    
class  SurveyAdmin(admin.ModelAdmin):
    fields = ['survey','author','pub_date']
    
    
class ChoiceInline(admin.StackedInline):
    model = Choice
    fields = ['choice','votes']
    extra = 3   

    
class PollAdmin(admin.ModelAdmin):
    fields = ['question','survey']
    inlines = [ChoiceInline]
    
class VoteAdmin(admin.ModelAdmin):
    fields = ['survey','username','comment']
    
    
    
admin.site.register(Survey,SurveyAdmin)
admin.site.register(Poll,PollAdmin)
admin.site.register(VoteRecord,VoteAdmin)