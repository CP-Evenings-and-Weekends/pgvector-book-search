import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_project.settings")
django.setup()

from books.models import Book
from books.embeddings import generate_embedding


books = [
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "A hobbit leaves his quiet home and joins an unexpected adventure involving dwarves, dangerous creatures, and a dragon.",
    },
    {
        "title": "Percy Jackson and the Olympians: The Lightning Thief",
        "author": "Rick Riordan",
        "description": "Percy Jackson discovers that he is a demigod and begins a dangerous quest involving Greek gods, monsters, friendship, and a stolen weapon.",
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "description": "Harry Potter discovers that he is a wizard and begins his first year at Hogwarts, where he learns magic, makes friends, and uncovers a dangerous mystery.",
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "Paul Atreides and his family travel to the desert planet Arrakis, where political conflict, survival, prophecy, and control of a valuable resource shape his destiny.",
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "description": "An astronaut is stranded alone on Mars and must use science, engineering, and determination to survive while NASA works to bring him home.",
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "Elizabeth Bennet navigates family expectations, relationships, social class, and misunderstandings while developing a complicated relationship with Mr. Darcy.",
    },
    {
        "title": "The Hound of the Baskervilles",
        "author": "Arthur Conan Doyle",
        "description": "Sherlock Holmes investigates a mysterious death and a frightening legend surrounding the Baskerville family estate in Victorian England.",
    },
    {
        "title": "The Name of the Rose",
        "author": "Umberto Eco",
        "description": "A monk investigates a series of mysterious deaths at a medieval monastery while uncovering secrets, forbidden knowledge, and a dangerous mystery.",
    },
    {
    "title": "Start With Why",
    "author": "Simon Sinek",
    "description": "A personal growth and leadership book about discovering your purpose, understanding why you do what you do, and using that purpose to guide meaningful action.",
    },
    {
    "title": "Marked",
    "author": "P.C. Cast and Kristin Cast",
    "description": "Zoey Redbird is Marked as a fledgling vampire and must begin her new life at the House of Night while dealing with friendship, romance, supernatural powers, and dangerous secrets.",
    },
    {
    "title": "Evermore",
    "author": "Alyson Noel",
    "description": "After a tragic accident, Ever Bloom discovers she can read people's thoughts and sense their auras, leading her into a supernatural world of immortals, romance, mystery, and self-discovery.",
    },
]


for book_data in books:
    book, created = Book.objects.get_or_create(
        title=book_data["title"],
        author=book_data["author"],
        defaults={"description": book_data["description"]},
    )

    if created:
        print(f"Creating embedding for: {book.title}")
        book.embedding = generate_embedding(book.description)
        book.save()
        print(f"Created: {book.title}")
    else:
        print(f"Already exists: {book.title}")
        
print("Finished loading books.")

