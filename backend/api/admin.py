from django.contrib import admin
from .models import Author, Book, AuthorBook

# Inline admin for AuthorBook
class AuthorBookInline(admin.TabularInline):  # Use TabularInline for a table-like display
    model = AuthorBook
    extra = 1  # Number of empty forms to display by default
    fields = ('book', 'contribution_percentage')
    autocomplete_fields = ['book']  # Enables autocomplete for book selection

# Admin for Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name in the list view
    search_fields = ('name',)  # Add search functionality for the name
    inlines = [AuthorBookInline]  # Include the inline for AuthorBook

# Admin for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_available')
    list_filter = ('is_available', 'published_date')  # Add filters for availability and date
    search_fields = ('title', 'description')  # Add search functionality
    autocomplete_fields = []  # Optional: Enable autocomplete fields if used elsewhere

# Admin for AuthorBook
@admin.register(AuthorBook)
class AuthorBookAdmin(admin.ModelAdmin):
    list_display = ('author', 'book', 'contribution_percentage')
    search_fields = ('author__name', 'book__title')  # Enable search by author name and book title
    autocomplete_fields = ['author', 'book']  # Enable autocomplete for author and book selection
    list_filter = ('contribution_percentage',)  # Optional: Add filters for contribution percentage
