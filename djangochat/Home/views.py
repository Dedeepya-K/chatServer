import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.mail import send_mail,EmailMessage

# Create your views here.
def index(request):

    all_clubs = Club.objects.all()

    context = {
        'all_clubs': all_clubs,
    }

    return render(request,"index.html", context)

# def addUser(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')

#         user = Profile(user = request.user, email = email)
#         user.save()
#         return redirect('index')
#     return render(request, 'addprofile.html')


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Enter Valid Username and Password!!")

    context = {}
    return render(request, "login.html", context)

def userLogout(request):
    return redirect('login')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created for '+ user)
            bio = "Hey I'm anonymous"
            usr = User.objects.get(username = user, email = email)
            p = Profile(user = usr)
            p.save()      
            return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)

def deleteClub(request,id):
    club = Club.objects.get(id=id)
    club.delete()
    return redirect('home')

    

def viewClub(request,id):
    club = Club.objects.get(id = id)


    name = club.club_name
    desc = club.club_description
    logo = club.club_logo
    leadid = club.club_lead_id
    clubid = club.id
    context = {'name':name, 'desc':desc, 'logo':logo, 'leadid':leadid, 'clubid':clubid}

    return render(request, "clubdet.html", context)
        

def add_event(request):
    if request.method == "POST":
        req = request.POST
        # Need to change the club
        club = Club.objects.all().first()
        # Creating an Event
        eve = Event(event_name = req["event_name"],event_description = req["event_description"],event_club = club,event_time = req["date_time"],event_photo = request.FILES['event_image'])
        eve.save()

        # Send Notifications
        mail_list_members = []
        members = club.member.all()
        print(members)
        for member in members:
            mail_list_members.append(member.email)
        mail_list_members.append("20131a1251@gvpce.ac.in")
        # mail_list_members.append("20131a4432@gvpce.ac.in")
        # mail_list_members.append("20131a05q0@gvpce.ac.in")
        print(mail_list_members)
        
        # Mail Details
        subject = f"{eve.event_name} by {club}"
        message = f"{club} is going to have {eve.event_name}-{eve.event_description} on {eve.event_time}"
        from_ad = os.environ.get('HOST_EMAIL')
        email = EmailMessage(subject,message,from_ad,mail_list_members)
        attachment = f"media/{eve.event_photo}"
        email.attach_file(attachment)
        email.send()

        print("EMAIL sent")
        return HttpResponse("Event Created and Notifications Sent")
    
    return render(request,"add_event.html")

def test(request):
    club = Club.objects.all().first()
    print(club.club_name)
    a = club.member.all().first()
    print(a)
    print(a.email)
    # return HttpResponse("OK")
    return render(request,"clubs.html")