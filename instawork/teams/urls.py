from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="detail"),
    path("signup/", views.signup_view, name="results"),
    path("addmember/", views.add_member, name="add_member"), 
    path('<int:pk>/update/', views.teamprofile_update.as_view(), name='teamprofile_update'),
    path('<int:pk>/delete/', views.teamprofile_delete.as_view(), name='teamprofile_delete'),
]