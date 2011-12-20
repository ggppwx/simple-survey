'''
Created on Dec 15, 2011

@author: roy
'''
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = patterns('surveys.views',
                        url(r'^$', 'home'),
                        url(r'^(?P<survey_id>\d+)/$','details'),
                        url(r'^(?P<survey_id>\d+)/showPollList$','show_poll_list'),
                        url(r'^(?P<survey_id>\d+)/vote','vote_for_survey'),
                        url(r'^(?P<survey_id>\d+)/thankyou','thankyou'),
                        url(r'^(?P<survey_id>\d+)/showResults','show_results'),
                        url(r'^createSurveyPage','create_a_survey_page'),
                        url(r'^createSurvey', 'create_a_survey'),
                        url(r'^(?P<survey_id>\d+)/deleteSurvey', 'delete_a_survey'),
                        
                        url(r'^(?P<survey_id>\d+)/createPollPage','create_a_poll_page'),
                        url(r'^(?P<survey_id>\d+)/createPoll','create_a_poll'),
                        url(r'^(?P<survey_id>\d+)/(?P<poll_id>\d+)/deletePoll','delete_a_poll'),
                        url(r'^logout', 'log_me_out'),
                        url(r'^registerPage', 'register_page'),
                        url(r'^register', 'register'),
                        url(r'^(?P<survey_id>\d+)/comment','comment'),
                       )
#if settings.DEBUG:
urlpatterns += patterns('',
                        (r'^login', 'django.contrib.auth.views.login',  {'template_name': 'login.html'} ),
                        
                        )
