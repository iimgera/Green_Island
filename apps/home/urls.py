from django.urls import path
from apps.home.views import (
    CategoryListView, SectionListView,
    RulesListView, ContactListView,
    PointListView,
)


urlpatterns = [
    path('category_section/', CategoryListView.as_view(), name='category'),
    path('sections/', SectionListView.as_view()),
    path('rules/', RulesListView.as_view()),
    path('contacts/', ContactListView.as_view()),
    path('points/', PointListView.as_view(), name='point-list'),
]
