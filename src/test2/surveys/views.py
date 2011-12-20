# Create your views here.
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from models import  Survey
from models import Poll
from models import Choice
from models import VoteRecord
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required



import datetime
import logging


logging.basicConfig(level=logging.DEBUG, format='%(message)s')



def home(request):
    # home page 
    # show account information
    # show survey list
    # can be redirected to login, register, vote, create 
    # @return: response to home.html
    
    # handle user information
    if request.user.is_authenticated():
        # show user information
        user = request.user
        # find all surveys 
        survey_list = Survey.objects.all()
        
        
        # get vote record
        vote_list = VoteRecord.objects.filter(username=user.username)
        voted_survey_ids = []
        for voteRec in vote_list:
            voted_survey_ids.append(voteRec.survey.id)
            
        # get expire list
        expired_list = __is_expired(survey_list)
        return render_to_response('home.html', {'user': user, 'survey_list':survey_list,'voted_list':voted_survey_ids,'expired_list':expired_list}, context_instance=RequestContext(request))
    else:
        # show login msg
        user = None
        return render_to_response('home.html', {'user': None}, context_instance=RequestContext(request))
                                               
def __is_expired(survey_list):                                               
    # check if the survey is expired     
    expired_list = []                          
    for s in survey_list:
        passDays = datetime.date.today().day - s.pub_date.day
        if passDays > 1:
            # expired
            expired_list.append(s.id)
    return expired_list 
        
def register_page(request):
    # register a new user 
    return render_to_response('register.html',context_instance=RequestContext(request))
    
def register(request):
    # process register information
    # create a user 
    logging.debug(request.POST)
    username = request.POST['Field1']
    email = ""
    password = request.POST['Field2']
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except:
        return render_to_response('register.html',{'error': 'maybe the user name has been used'},context_instance=RequestContext(request))
    # login 
    my_user = authenticate(username=username, password=password)
    if user is not None:
        login(request, my_user)
        return HttpResponseRedirect('/surveys')
    else:
        return HttpResponse('error register fail')
    
    
'''
def log_me_in_page(request):
    # redirected to login page 
    return render_to_response('login.html', context_instance=RequestContext(request))
'''
''' 
def log_me_in(request):
    # login 
    # @param request: request from login page 
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('success')
        else:
            # user has been disabled 
            return HttpResponse('disabled user')
    else:
        # invalid login 
        return HttpResponse('invalid login')
'''



@login_required(login_url='/surveys/login') 
def log_me_out(request):
    # logout the system
    logout(request)
    # redirect ?
    return HttpResponseRedirect('/surveys/')
   
'''
def vote(request, poll_id):
    # vote for the a poll in a survey 
    # @param poll_id: the id of a poll, it's unique
    # get the choice from a from in html side, update it to database
    # return to next question.   
    p = get_object_or_404(Poll,pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice']) # which is a choice object
        selected_choice.votes += 1
        selected_choice.save()
    
    except:
        return
    
'''
    
@login_required(login_url='/surveys/login') 
def vote_for_survey(request, survey_id):    
    # vote for a survey
    pollCount = int(request.POST['pollCount'])
    s = get_object_or_404(Survey, pk=survey_id)
    logging.debug(request.POST)
    logging.debug(pollCount)
    
    for i in range(pollCount):
        postFix = str(i+1)
        logging.debug(postFix)
        if 'Questions'+postFix in request.POST:
            try:
                p = s.poll_set.all().get(pk=request.POST['Questions'+postFix])
            except:
                return HttpResponse('error')
        else:
            continue
            
        if 'Field'+postFix in request.POST:
            logging.debug('this field exist')
            try:
                selected_choice = p.choice_set.get(pk=request.POST['Field'+postFix])
                selected_choice.votes += 1
                selected_choice.save() # save to database
            except:
                return HttpResponse('error')

        else:
            continue
    # get comment 
    comment = escape(str(request.POST['Comment0']))
    logging.debug("--------------------------------"+comment)
    commentFommat =  "<li id='foli1' class='notranslate'><p>"+str(request.user.username)+':</p><p>'+comment +'</p></li>'
    
    if s.comment:
        s.comment += commentFommat
    else:
        s.comment = commentFommat
    #s.comment = s.comment + "<div>"+ str(request.user.username)+": </div>"+"<div>"+comment +"</div>"
    
    # update the vote record 
    voterecord = VoteRecord(survey=s,username=request.user.username,comment=str(request.POST['Comment0']))
    voterecord.save()
    
    
    # before redirect to thank you, make the popularity +1
    s.popularity += 1
    s.save()
    
    return HttpResponseRedirect(reverse('surveys.views.thankyou',args=(survey_id,)))
        

def thankyou(request,survey_id):
    # show thank you 
    return render_to_response('thankYou.html',{'survey_id':survey_id}, context_instance=RequestContext(request))

@login_required(login_url='/surveys/login') 
def comment(request, survey_id):
    # show comment of a survey
    s = get_object_or_404(Survey, pk=survey_id)
    comment = s.comment
    return render_to_response('comment.html',{'survey_comment':comment}, context_instance=RequestContext(request))

@login_required(login_url='/surveys/login') 
def show_results(request, survey_id):
    # show results of a survey
    # @param survey_id: the unique survey id
    # display all the polls of a survey and their results. 
    s = get_object_or_404(Survey,pk = survey_id)
    return render_to_response('result.html', {'survey':s ,'poll_list': s.poll_set.all()},context_instance=RequestContext(request))
    
def details(request, survey_id):
    # show details of a survey 
    s = get_object_or_404(Survey,pk=survey_id)
    return render_to_response('details.html',{'survey':s})

@login_required(login_url='/surveys/login') 
def show_survey_list(request):
    # show all surveys in a list
    # this view is to show a general view of all surveys
    survey_list = Survey.objects.all()
    return render_to_response('sth.html', {'survey_list': survey_list})


@login_required(login_url='/surveys/login') 
def show_poll_list(request, survey_id):
    # show all polls in a survey
    # which is implemented in details
    # each poll has several choices, which is contained in p.choice_set
    # @param survey_id: input survey id 
    # response: 
    # survey: survey object,  poll_list: a list of all polls in this survey
    # sth.html: a template show all the questions in a survey   
    s = get_object_or_404(Survey,pk=survey_id)
    return render_to_response('votePage.html', {'survey':s ,'poll_list': s.poll_set.all()},context_instance=RequestContext(request))

@login_required(login_url='/surveys/login') 
def create_a_survey_page(request):
    # render createSurvey.html
    survey_list = Survey.objects.filter(author=request.user.username)
    return render_to_response('createSurvey.html', {'my_survey_list':survey_list,'user':request.user},context_instance=RequestContext(request))

@login_required(login_url='/surveys/login') 
def create_a_survey(request):
    # create a survey 
    # create a survey object
    # get input from createSurvey.html
    # return HttpResponse('create a survey ')
    logging.debug(request.POST)
    survey_name = request.POST['SurveyName']
    s = Survey(survey=survey_name, pub_date=datetime.date.today(), author=request.user.username, popularity=0)
    s.save()

    # response to /s.id/addPolls
    return HttpResponseRedirect('createSurveyPage')

@login_required(login_url='/surveys/login') 
def delete_a_survey(request, survey_id):
    # delete a survey
    
    s = get_object_or_404(Survey, pk=survey_id)
    # check if the user has the permission to this survey
    if s.author == request.user.username:
        s.delete()
        return HttpResponseRedirect('/surveys/createSurveyPage')
    else:
        return
    
    
@login_required(login_url='/surveys/login')     
def create_a_poll_page(request,survey_id):
    # show all polls in this survey
    s = get_object_or_404(Survey, pk=survey_id)
    # check if the user is correct
        
    return render_to_response('addPolls.html',{'survey_id':survey_id,'poll_list':s.poll_set.all(),'user':request.user},context_instance=RequestContext(request))
    
@login_required(login_url='/surveys/login') 
def create_a_poll(request,survey_id):
    # create a poll in a survey 
    # get questions from input 
    # redirect to craetPollPage
    
    
    logging.debug(request.POST)
    question = request.POST['Question0']
    choice_list = request.POST.getlist('Field1')
    s = get_object_or_404(Survey,pk = survey_id)
    # check if user correct
    if not s.author == request.user.username:
        return 
    
    p = Poll(survey=s, question = question)
    p.save()
    # get choice from form input
    logging.debug(choice_list)
    for c in choice_list:
        if c:
            logging.debug(c)
            choice = Choice(poll= p,  choice = c, votes=0)
            choice.save()
    
     
    return HttpResponseRedirect('createPollPage')
    # return HttpResponse('create a poll')

@login_required(login_url='/surveys/login') 
def delete_a_poll(request, survey_id, poll_id):
    # delete a poll in a survey
    s = get_object_or_404(Survey, pk=survey_id)
    if s.author == request.user.username:
        p = get_object_or_404(Poll, pk=poll_id)
        p.delete()
        return HttpResponseRedirect('/surveys/'+survey_id+'/createPollPage')
    else:
        return
    
    
    
    
