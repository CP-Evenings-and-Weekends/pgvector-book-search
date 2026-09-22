from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document
from .embeddings import generate_embedding
from pgvector.django import CosineDistance


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "author", "description"]


@api_view(["POST"])
def create_document(request):
    serializer = DocumentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    doc = serializer.save()

    # Generate and store the embedding
    doc.embedding = generate_embedding(doc.content)
    doc.save(update_fields=["embedding"])

    return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def search_documents(request):
    query = request.query_params.get("q", "")
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate embedding for the search query
    query_embedding = generate_embedding(query)

    # Find the most similar documents
    results = (
        Document.objects.annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:5]
    )

    data = [
        {
            "id": doc.id,
            "title": doc.title,
            "author": doc.author,
            "description": doc.description,
        }
        for doc in results
    ]

    return Response(data)