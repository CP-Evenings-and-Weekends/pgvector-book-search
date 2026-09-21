# pgvector Book Search

Apply today's [Embeddings + pgvector lesson](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_06_AI_LLMs/week17/day1/README.md) to a book search problem, then prove to yourself that semantic search actually beats keyword search.

The default plan is to build tonight's work **inside the practice project you made in class**, so there is no new scaffolding, no new container, and no new `.env` on a Monday night. This repo also ships a `docker-compose.yml`, `requirements.txt`, and `.env.example` as a fallback if your class environment never got working.

## Setup (default path: extend your class project)

In the `vector_demo` project from class, with its Docker container still running:

```bash
python manage.py startapp books
```

Then wire it up with the same pattern from the lesson:

1. Add `"books"` to `INSTALLED_APPS`
2. Build a `Book` model with `title`, `author`, `description` (TextField), and `embedding = VectorField(dimensions=1536, null=True, blank=True)` — use `768` if your class project is on the Ollama path, matching what you already migrated
3. Run `python manage.py makemigrations books && python manage.py migrate` (no migration edit needed this time: your class project's first migration already enabled the pgvector extension)
4. Wire `path("api/", include("books.urls"))` in your project `urls.py`
5. Reuse the `generate_embedding` helper from class — import it from `search.embeddings`, or copy the file into `books/`

## Setup (fallback path: fresh scaffold)

Only if your class environment broke and you cannot fix it quickly:

```bash
cp .env.example .env
# Put your LLM_API_KEY in .env (Ollama works too, see below)
docker compose up -d
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
django-admin startproject book_search .
python manage.py startapp books
```

On this path, also update `DATABASES` to point at the pgvector container, and make sure the initial migration includes `VectorExtension()` at the top of `operations`, exactly as in the lesson.

If you'd rather use Ollama for embeddings (free, no API key), see the bottom of this README.

## Assignment 1 — Book semantic search

Build a Django + DRF API that stores books and finds the 3 most similar to a search term.

### Required endpoints

| Method | Path | Behavior |
|---|---|---|
| `POST` | `/api/books/` | Create a book; generate + store the embedding from the `description` |
| `GET`  | `/api/books/` | List all books (no embeddings in the response — they're huge) |
| `GET`  | `/api/books/search/?q=<query>` | Return the 3 most semantically similar books to `q`, each with its distance score |

### Seed data

Insert **at least 10 books** across different genres so the search has something to differentiate.  Vary the descriptions deliberately — keep some sci-fi-ish, some historical, some self-help, etc.  Save a `seed.json` or a `setup_data.py` you can re-run.

### Verify

```bash
# 1. Seed your 10 books
python setup_data.py

# 2. Search using words that don't appear in any description
curl "http://localhost:8000/api/books/search/?q=interstellar+adventure"
curl "http://localhost:8000/api/books/search/?q=personal+growth+and+habits"
curl "http://localhost:8000/api/books/search/?q=victorian+era+mystery"
```

Each result should include `id`, `title`, `author`, and `distance` (cosine distance — lower is more similar).

## Assignment 2 — Keyword vs semantic comparison

Add a **second** search endpoint that does plain `ILIKE` keyword matching, then run both searches against the same queries and document where semantic wins.

### Required endpoint

`GET /api/books/keyword-search/?q=<query>` — uses `Book.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))[:3]`.

### Compare

Create a `comparison.md` in your repo with **at least 3 cases** where semantic search finds a meaningfully better result than keyword search.  For each case:

- The query
- The top 3 keyword results
- The top 3 semantic results
- A one-sentence note on *why* semantic was better (synonym match? abbreviation? conceptual relation?)

Good queries to try (none of these are likely to appear literally in your descriptions): *"book about WWII"*, *"page-turner for the beach"*, *"how to be productive"*, *"AI takeover"*.

## Using Ollama for embeddings (no API key)

If you extended your class project, this decision is already made: keep the provider and dimension count your project already uses (768 for the Ollama path), and you are done here.

On the fresh-scaffold path, if you don't want to pay or sign up for an API:

```bash
ollama pull nomic-embed-text
```

Then in your `.env`:

```
LLM_API_BASE_URL=http://localhost:11434
LLM_API_KEY=unused
EMBEDDING_MODEL=nomic-embed-text
```

`nomic-embed-text` produces **768-dim** vectors, not 1536, so adjust the `VectorField(dimensions=768, ...)` on the `Book` model.  If you already migrated at 1536, nuke your DB volume (`docker compose down -v`) and re-migrate.

## Things to think about
- Why is the embedding stored once on insert and not recomputed on every search?  What would it cost if you regenerated it every request?
- Cosine **distance** (what pgvector uses with `<=>`) vs cosine **similarity** (the score 0–1 we discussed in the lesson) — what's the relationship?  Why does the lesson sort ascending?
- If two books have similar titles but very different descriptions, which one will rank higher in semantic search?  Why?
- Your seed is 10 books.  How would the same code behave at 10,000?  100,000?  Where does it start hurting, and what would you add (index? pre-filter?) to make it fast?

## Stretch
- Add an HNSW index on the `embedding` column.  Measure search time before vs after with `EXPLAIN ANALYZE`.
- Allow `?k=10` to control the result count.
- Add a `genre` field and a hybrid endpoint: filter by genre via SQL first, then semantic-search within the filtered set.
- Switch from `text-embedding-3-small` (1536d) to `text-embedding-3-large` (3072d) and compare quality on the same queries.  Worth the cost?

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
