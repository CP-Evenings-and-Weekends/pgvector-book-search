from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.books, name="books"),
    path("books/<book_id>/", views.get_book, name="get-book"),
]