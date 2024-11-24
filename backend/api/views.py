from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Author, Book, AuthorBook
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
import json

# test view
def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

# Helper function to parse JSON request body
def parse_request_body(request):
    return json.loads(request.body.decode('utf-8'))

# Author CRUD
def author_list(request):
    if request.method == 'GET':
        # Use Prefetch to optimize querying related books
        authors = Author.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.only('id', 'title'))
        ).values('id', 'name', 'bio', 'books__id', 'books__title')

        # Process authors into a structured format
        authors_with_books = {}
        for author in authors:
            author_id = author['id']
            if author_id not in authors_with_books:
                authors_with_books[author_id] = {
                    'id': author_id,
                    'name': author['name'],
                    'bio': author['bio'],
                    'books': []
                }
            if author['books__id']:
                authors_with_books[author_id]['books'].append({
                    'id': author['books__id'],
                    'title': author['books__title']
                })

        # Convert to a list of authors
        authors_list = list(authors_with_books.values())
        return JsonResponse({'authors': authors_list}, safe=False)

@csrf_exempt
def author_create(request):
    if request.method == 'POST':
        data = parse_request_body(request)
        author = Author.objects.create(name=data['name'], bio=data.get('bio'))
        return JsonResponse({'id': author.id, 'name': author.name, 'bio': author.bio})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return JsonResponse({'id': author.id, 'name': author.name, 'bio': author.bio})

@csrf_exempt
def author_update(request, pk):
    if request.method == 'PUT':
        data = parse_request_body(request)
        author = get_object_or_404(Author, pk=pk)
        author.name = data.get('name', author.name)
        author.bio = data.get('bio', author.bio)
        author.save()
        return JsonResponse({'id': author.id, 'name': author.name, 'bio': author.bio})

@csrf_exempt
def author_delete(request, pk):
    if request.method == 'DELETE':
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return JsonResponse({'message': 'Author deleted successfully'})

# Book CRUD
def book_list(request):
    if request.method == 'GET':
        books = list(Book.objects.values('id', 'title', 'published_date', 'description', 'is_available'))
        return JsonResponse({'books': books}, safe=False)

@csrf_exempt
def book_create(request):
    if request.method == 'POST':
        data = parse_request_body(request)
        book = Book.objects.create(
            title=data['title'],
            published_date=data.get('published_date'),
            description=data.get('description'),
            is_available=data.get('is_available', True)
        )
        return JsonResponse({'id': book.id, 'title': book.title, 'published_date': book.published_date, 'description': book.description, 'is_available': book.is_available})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return JsonResponse({'id': book.id, 'title': book.title, 'published_date': book.published_date, 'description': book.description, 'is_available': book.is_available})

@csrf_exempt
def book_update(request, pk):
    if request.method == 'PUT':
        data = parse_request_body(request)
        book = get_object_or_404(Book, pk=pk)
        book.title = data.get('title', book.title)
        book.published_date = data.get('published_date', book.published_date)
        book.description = data.get('description', book.description)
        book.is_available = data.get('is_available', book.is_available)
        book.save()
        return JsonResponse({'id': book.id, 'title': book.title, 'published_date': book.published_date, 'description': book.description, 'is_available': book.is_available})

@csrf_exempt
def book_delete(request, pk):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'})

# AuthorBook CRUD
@csrf_exempt
def author_book_list(request):
    if request.method == 'GET':
        author_books = list(AuthorBook.objects.values('id', 'author_id', 'author__name', 'book_id', 'book__title', 'contribution_percentage'))
        return JsonResponse({'author_books': author_books}, safe=False)

@csrf_exempt
def author_book_create(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body.decode('utf-8'))

            # Check for required fields
            if 'author_id' not in data or 'book_id' not in data:
                return JsonResponse(
                    {'error': 'Missing required fields: author_id and book_id.'},
                    status=400
                )

            # Get the author and book objects
            author = get_object_or_404(Author, id=data['author_id'])
            book = get_object_or_404(Book, id=data['book_id'])

            # Get the contribution percentage if provided
            contribution_percentage = data.get('contribution_percentage', None)

            # Validate contribution_percentage if provided
            if contribution_percentage is not None:
                if not isinstance(contribution_percentage, int) or not (0 <= contribution_percentage <= 100):
                    return JsonResponse(
                        {'error': 'Contribution percentage must be an integer between 0 and 100.'},
                        status=400
                    )

            # Check for duplicate relationships
            if AuthorBook.objects.filter(author=author, book=book).exists():
                return JsonResponse(
                    {'error': 'This author-book relationship already exists.'},
                    status=400
                )

            # Create the AuthorBook relationship
            author_book = AuthorBook.objects.create(
                author=author,
                book=book,
                contribution_percentage=contribution_percentage
            )

            # Return success response
            return JsonResponse({
                'id': author_book.id,
                'author_id': author.id,
                'book_id': book.id,
                'author_name': author.name,
                'book_title': book.title,
                'contribution_percentage': contribution_percentage
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON format.'},
                status=400
            )
        except ValidationError as e:
            return JsonResponse(
                {'error': f'Validation error: {e.messages}'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=500
            )
    else:
        return JsonResponse(
            {'error': 'Method not allowed. Only POST requests are allowed.'},
            status=405
        )

@csrf_exempt
def author_book_update(request, pk):
    if request.method == 'PUT':
        try:
            # Parse the request body
            data = json.loads(request.body.decode('utf-8'))

            # Get the AuthorBook instance
            author_book = get_object_or_404(AuthorBook, pk=pk)

            # Update author if `author_id` is provided
            if 'author_id' in data:
                try:
                    author = get_object_or_404(Author, pk=data['author_id'])
                    author_book.author = author
                except ValidationError:
                    return JsonResponse(
                        {'error': 'Invalid author ID.'},
                        status=400
                    )

            # Update book if `book_id` is provided
            if 'book_id' in data:
                try:
                    book = get_object_or_404(Book, pk=data['book_id'])
                    author_book.book = book
                except ValidationError:
                    return JsonResponse(
                        {'error': 'Invalid book ID.'},
                        status=400
                    )

            # Update contribution_percentage if provided
            contribution_percentage = data.get('contribution_percentage', author_book.contribution_percentage)
            if contribution_percentage is not None:
                if not isinstance(contribution_percentage, int) or not (0 <= contribution_percentage <= 100):
                    return JsonResponse(
                        {'error': 'Contribution percentage must be an integer between 0 and 100.'},
                        status=400
                    )
                author_book.contribution_percentage = contribution_percentage
                
            if AuthorBook.objects.filter(author=author, book=book).exists():
                return JsonResponse(
                    {'error': 'This author-book relationship already exists.'},
                    status=400
                )

            # Save the updated AuthorBook
            author_book.save()

            # Return success response
            return JsonResponse({
                'id': author_book.id,
                'author_id': author_book.author.id,
                'book_id': author_book.book.id,
                'author_name': author_book.author.name,
                'book_title': author_book.book.title,
                'contribution_percentage': author_book.contribution_percentage
            })

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON format.'},
                status=400
            )
        except ValidationError as e:
            return JsonResponse(
                {'error': f'Validation error: {e.messages}'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=500
            )
    else:
        return JsonResponse(
            {'error': 'Method not allowed. Only PUT requests are allowed.'},
            status=405
        )



@csrf_exempt
def author_book_delete(request, pk):
    if request.method == 'DELETE':
        author_book = get_object_or_404(AuthorBook, pk=pk)
        author_book.delete()
        return JsonResponse({'message': 'AuthorBook deleted successfully'})
    
def author_book_detail(request, pk):
    author_book = get_object_or_404(AuthorBook, pk=pk)
    return JsonResponse({'id': author_book.id, 'author_id': author_book.author_id, 'book_id': author_book.book_id, 'contribution_percentage': author_book.contribution_percentage})