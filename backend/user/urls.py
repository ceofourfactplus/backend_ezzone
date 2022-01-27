from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.RegisterUserAPIView.as_view()),
  path('conf-pas/', views.ConfirmPass.as_view()),
  path('login/', views.IsActive.as_view()),
  path('read-all/', views.UserList.as_view()),
  path('search-name/<str:qury>', views.SearchName.as_view()), 
  path('edit-user/<int:pk>',views.EditUser.as_view()),
  path('change-status/<int:pk>/<int:status>', views.ChangeStatus.as_view())
]