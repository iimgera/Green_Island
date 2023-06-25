from django.urls import path, include
from rest_framework import routers

from apps.users import views


app_name = 'users'


router = routers.DefaultRouter()
router.register(r'client-profile', views.ClientProfileViewSet, basename='client-profile')

urlpatterns = [
    path('', include(router.urls)),
]


urlpatterns = [
    path('operators/', views.OperatorListView.as_view(), name='operator-list'),
    path('operators/register/', views.OperatorRegisterView.as_view(), name='operator-reg'),
    path('operators/<int:pk>/', views.OperatorDetailView.as_view(), name='operator-detail'),

    path('brigades/', views.BrigadeListView.as_view(), name='brigade-list'),
    path('brigades/<int:pk>/', views.BrigadeDetailView.as_view(), name='brigade-detail'),
    path('brigades/register/', views.BrigadeRegisterView.as_view(), name='brigade-reg'),

    path('', include(router.urls)),
    path('clients/register/', views.ClientRegisterView.as_view(), name='client-reg'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view(), name='reset-password'),
]
