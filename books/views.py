from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Book
from .embeddings import generate_embedding
from pgvector.django import CosineDistance


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "description"]


@api_view(["GET", "POST"])
def books_collection(request):
    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book.embedding = generate_embedding(book.description)
        book.save(update_fields=["embedding"])
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

    books = Book.objects.all()
    return Response(BookSerializer(books, many=True).data)


@api_view(["GET"])
def search_books(request):
    query = request.query_params.get("q", "")
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    query_embedding = generate_embedding(query)

    results = (
        Book.objects.annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:3]
    )

    data = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "distance": float(book.distance),
        }
        for book in results
    ]

    return Response(data)


@api_view(["GET"])
def keyword_search_books(request):
    query = request.query_params.get("q", "")
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )[:3]

    return Response(BookSerializer(results, many=True).data)