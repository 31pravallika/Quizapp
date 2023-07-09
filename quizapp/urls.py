from django.urls import path,re_path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('home',views.home,name="home"),
    path('home/quiz/<cid>',views.quiz,name="quiz"),
    path('profile/<uid>',views.profile,name="profile"),
    path('add/<cid>',views.add,name="add"),
    path('correct/<cid>',views.correct,name="correct"),
    
]