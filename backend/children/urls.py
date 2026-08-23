from django.urls import path
from .views import ChildCreateView, ChildSearchView

urlpatterns = [
    path('add/', ChildCreateView.as_view(), name='add-child'),
    path('search/', ChildSearchView.as_view(), name='search-child'),
]
