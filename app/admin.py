from django.contrib import admin
from .models import Book, Rent, Genre, BookInstance, Reader

# Register your models here.

admin.site.register(Book)
admin.site.register(Rent)
admin.site.register(Genre)
admin.site.register(BookInstance)

admin.site.register(Reader)