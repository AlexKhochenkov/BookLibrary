from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import Book, BookInstance, Reader, Genre, Rent
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise ValidationError('Wrong password')
        return data

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields =['name', 'reader_number']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReaderForm, self).__init__(*args, **kwargs)

    def clean_reader_number(self):
        # Проверка и получение или создание 
        reader_num = self.cleaned_data['reader_number']
        try:
            reader = Reader.objects.get(reader_number=reader_num)
        except Reader.DoesNotExist:
            return reader_num
        raise ValidationError('Такой номер уже существует')
    
    def save(self, commit=True):


        reader = super(ReaderForm, self).save(commit=False)
        reader.reader_number = self.cleaned_data['reader_number']
        

        if commit:
            reader.save()

        return reader
    
class BookForm(forms.ModelForm):
    instances = forms.IntegerField(required=True)
    genres = forms.CharField(max_length=16, required=True)

    class Meta:
        model = Book
        fields =['title', 'content', 'author', 'genres']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BookForm, self).__init__(*args, **kwargs)

    def clean_instances(self):
        # Проверка и получение или создание 
        inst = self.cleaned_data['instances']
        if inst<=0:
            raise ValidationError('Введите положительное количество')
        else:
            return inst
        
    def clean_genres(self):
        # Проверка и получение или создание объекта Reader
        genres_name = self.cleaned_data['genres']
        try:
            genre = Genre.objects.get(name=genres_name)
        except Genre.DoesNotExist:
            raise forms.ValidationError('Жанр с таким именем не найден.')
        return genre
    
    def save(self, commit=True):


        book = super(BookForm, self).save(commit=False)
        book.genres = self.cleaned_data['genres']
        

        if commit:
            book.save()
        for i in range(self.cleaned_data['instances']):
            inst=BookInstance.objects.create(book=book)
            inst.save()

        return book

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password and password_check and password != password_check:
            raise ValidationError("Passwords don't match")

        return cleaned_data
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user

class RentForm(forms.ModelForm):
    reader = forms.CharField(max_length=64, required=True)
    book = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Rent
        fields = ['reader']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RentForm, self).__init__(*args, **kwargs)

    def clean_reader(self):
        # Проверка и получение или создание объекта Reader
        reader_name = self.cleaned_data['reader']
        try:
            reader = Reader.objects.get(name=reader_name)
        except Reader.DoesNotExist:
            raise forms.ValidationError('Читатель с таким именем не найден.')
        return reader

    def clean_book(self):
        # Проверка и получение объекта Book
        book_name = self.cleaned_data['book']
        try:
            book = Book.objects.get(title=book_name)
        except Book.DoesNotExist:
            raise forms.ValidationError('Книга с таким названием не найдена.')
        bookinstances = BookInstance.objects.filter(book=book, rent=None).first()
        if not bookinstances:
            raise forms.ValidationError('Нет свободных экземпляров')
        return book

    def save(self, commit=True):


        rent = super(RentForm, self).save(commit=False)
        rent.reader = self.cleaned_data['reader']
        book = self.cleaned_data['book']
        bookinstances = BookInstance.objects.filter(book=book, rent=None).first()
        rent.bookinstance = bookinstances
        rent.user = self.request.user
        rent.date_taken = timezone.now()

        if commit:
            rent.save()

        return rent
