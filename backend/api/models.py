from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    books = models.ManyToManyField(
        'Book',
        through='AuthorBook',
        related_name='authors'
    )  # Using ManyToManyField with a through model

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AuthorBook(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contribution_percentage = models.IntegerField(null=True, blank=True)  # Extra field

    class Meta:
        unique_together = ('author', 'book')  # Ensures no duplicate relationships

    def __str__(self):
        return f"{self.author.name} - {self.book.title}"
