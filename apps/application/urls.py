from django.urls import path
from apps.application import views


urlpatterns = [
    path('client/application/create/', views.ClientApplicationCreateAPIView.as_view(), name='client-application-create'),

    path('applications/', views.ApplicationListAPIView.as_view(), name='application-list'),
    path('operator/<int:pk>/my_applications/', views.AssignOperatorAPIView.as_view(), name='assign-operator'),

    path('add_brigade/<int:pk>/', views.AddBrigadeAPIView.as_view(), name='add-brigade'),
    path('brigade/<int:pk>/status/', views.BrigadeStatusUpdateView.as_view(), name='brigade-status-update'),
    path('in_progressing_status/<int:pk>/', views.BrigadeApplicationStatusUpdateAPIView.as_view(), name='application-in_progressing-status'),

    path('all_applications/', views.AllApplicationAPIView.as_view(), name='all-applications'),
    path('change_status/<int:pk>/', views.ApplicationStatusUpdateAPIView.as_view(), name='update-application-status'),
]
