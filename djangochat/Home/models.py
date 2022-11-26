from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=100)
    club_lead_id = models.PositiveIntegerField(blank=True)
    club_description = models.CharField(max_length=500,blank=True)
    club_logo = models.ImageField(upload_to="images",blank=True)
    club_acronym = models.CharField(max_length=10,blank=True)
    club_mail = models.EmailField(max_length = 254, default="abc@gmail.com")  
    def __str__(self):
        return f'{self.club_name} Club'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=100,default="Hey! I'm new here")
    clubs_member = models.ManyToManyField(Club,related_name="member")
    clubs_core_member = models.ManyToManyField(Club,blank=True,related_name="core_member")
    clubs_lead = models.ManyToManyField(Club,blank=True,related_name="lead")
    profile_photo = models.ImageField(upload_to="images",blank=True)
    email = models.EmailField(max_length = 254, default="abc@gmail.com")  

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.CharField(max_length=500)
    event_club = models.ForeignKey(Club,on_delete=models.CASCADE,related_name="club") ## Correct
    event_time = models.DateTimeField()
    event_photo = models.ImageField(upload_to="images",blank=True)

    def __str__(self):
        return f"{self.event_club}'s Event"