from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.books_collection, name="books-collection"),
    path("books/search/", views.search_books, name="search-books"),
    path("books/keyword-search/", views.keyword_search_books, name="keyword-search-books"),
]