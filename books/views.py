from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pgvector.django import CosineDistance

from .models import Book
from .serializers import BookSerializer
from .embeddings import generate_embedding


@api_view(["GET", "POST"])
def books(request):

    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.save()

        try:
            # Generate and store the embedding
            book.embedding = generate_embedding(book.description)
            book.save(update_fields=["embedding"])

        except Exception as e:
            book.delete()
            return Response(
                {"error": f"Could not generate embedding: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            BookSerializer(book).data,
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
def search_books(request):

    query = request.query_params.get("q", "")

    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate embedding for the search query
    query_embedding = generate_embedding(query)

    # Find the 3 most similar books
    results = (
        Book.objects
        .annotate(
            distance=CosineDistance("embedding", query_embedding)
        )
        .order_by("distance")[:3]
    )

    data = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
        }
        for book in results
    ]

    return Response(data)