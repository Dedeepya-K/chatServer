from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="home"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
    path('delete_club/<int:id>/', views.deleteClub, name="deleteclub"),  
    path('club/<int:id>/', views.viewClub, name="viewclub"),
    path('add_event/',views.add_event,name="add_event"),
    path('test',views.test),
]
