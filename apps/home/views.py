from rest_framework import generics

from apps.home.models import (
    Section, Rules,
    Contact, Point,
    Category,
)
from apps.home.serializers import (
    SectionSerializer, RulesSerializer,
    ContactSerializer, PointSerializer,
    CategorySerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class RulesListView(generics.ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer


class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PointListView(generics.ListAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
