from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.db import models

# Create your models here.

class BookManager(models.Manager):
    def calculate_rating(self):
        books = Book.objects.annotate(
            raiting=Coalesce(Count('bookinstances'),0)-
            Coalesce(Count('bookinstances__rent'), 0)
        )
        return books

    def available(self):
        books = self.calculate_rating()
        return books.order_by('-raiting')

    def genre(self, genre):
        books = self.calculate_rating()
        books = books.filter(genres__name=genre)
        return books.order_by('-raiting')
    
class GenreManager(models.Manager):
    def calculate_books(self):
        genres = self.annotate(
            book_num=Coalesce(Count('book'), 0)
        )
        return genres

    def hot(self):
        genres = self.calculate_books()
        return genres.order_by('-book_num')[:5]

class Reader(models.Model):
    name = models.CharField(max_length=64)
    reader_number = models.IntegerField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=256)
    author=models.CharField(max_length=16) 
    genres = models.ForeignKey('Genre', related_name='books', on_delete=models.PROTECT)

    objects=BookManager()

    def __str__(self):
        return self.title
    
class BookInstance(models.Model):
    book = models.ForeignKey('Book', related_name='bookinstances', on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

class Rent(models.Model):
    date_taken=models.DateField() 
    bookinstance = models.OneToOneField('BookInstance', related_name='rent', 
                                        on_delete=models.CASCADE)
    user = models.ForeignKey(User, max_length=256, related_name='rents', null=True, 
                             blank=True, on_delete=models.SET_NULL)
    reader = models.ForeignKey('Reader', max_length=256, related_name='rents', 
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.bookinstance.book.title + ' ' + self.reader.name

class Genre(models.Model):
    name = models.CharField(max_length=16)

    objects=GenreManager()

    def __str__(self):
        return self.name

    

