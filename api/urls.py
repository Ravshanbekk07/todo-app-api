from django.urls import path
from .views import UsersView,TaskView,LoginView

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UsersView.as_view()),

    path('tasks/',TaskView.as_view()),
    path('tasks/<int:pk>/',TaskView.as_view()),

    path("userlogin/",LoginView.as_view())

]
