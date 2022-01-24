from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('list/', views.ListUserView.as_view(), name='list'),
    path('list/<int:pk>/', views.RetrieveUserView.as_view(), name='list-detail'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('update/<int:pk>/', views.RetrieveUpdateUserView.as_view(), name='user-detail'),
]