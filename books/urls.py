from django.urls import path
from .views import books


urlpatterns = [
    path("books/", books, name="books"),
]

