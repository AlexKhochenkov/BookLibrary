from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
import math
from django.db.models import Sum
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from app.forms import LoginForm, RentForm, ReaderForm, BookForm, UserForm
from .models import User
from .models import Book, Rent, Genre, BookInstance, Reader

# Create your views here.

genres_all=Genre.objects.all()

def paginate(request, objects, per_page=5):
    limit=math.ceil(len(objects)/per_page)
    paginator = Paginator(objects, per_page)

    page = request.GET.get('page', 1)
    try:
        if int(page)>limit or int(page)<=0:
            return {'content': paginator.page(1), 'page': int(page), 'limit': limit}
        return {'content': paginator.page(page), 'page': int(page), 'limit': limit}
    except ValueError:
        return {'content': paginator.page(1), 'page': int(page), 'limit': limit}

def index(request):
    return render(request, "index.html",
                  {'genres': genres_all})

@login_required(login_url="/login", redirect_field_name='continue')
def books(request):
    page_params = paginate(request, Book.objects.available())
    return render(request, "books.html", 
                  {'books': page_params['content'],
                   'genres': genres_all,  
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})

def books_adminka(request):
    page_params = paginate(request, Book.objects.available())
    return render(request, "books-adminka.html", 
                  {'books': page_params['content'],
                   'genres': genres_all,  
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})

def users(request):
    page_params = paginate(request, User.objects.all())
    return render(request, "users.html", 
                  {'users': page_params['content'],
                   'genres': genres_all,  
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})

@login_required(login_url="/login", redirect_field_name='continue')
def readers(request):
    page_params = paginate(request, Reader.objects.all())
    return render(request, "readers.html", 
                  {'readers': page_params['content'], 
                   'genres': genres_all, 
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})

@login_required(login_url="/login", redirect_field_name='continue')
def genres(request, genre_name):
    items=Book.objects.genre(genre_name)
    page_params=paginate(request, items)
    return render(request, "genres.html", 
                    {'books': page_params['content'], 
                   'genres': genres_all, 
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit'], 
                    'genre': genre_name})

@csrf_protect
def rent_create(request):
    # Получаем объект Book по его ID

    if request.method == 'POST':
        form = RentForm(request.POST, request=request)
        if form.is_valid():
            rent = form.save()
            return redirect(reverse('index'))  # Замените 'some_success_url' на нужный URL
    else:
        form = RentForm(request=request)

    return render(request, 'rent-create.html', {'form': form})

@csrf_protect
def book_create(request):

    if request.method == 'POST':
        form = BookForm(request.POST, request=request)
        if form.is_valid():
            book = form.save()
            return redirect(reverse('adminka'))  # Замените 'some_success_url' на нужный URL
    else:
        form = BookForm(request=request)

    return render(request, 'book-create.html', {'form': form})

@csrf_protect
def user_create(request):

    if request.method == 'POST':
        form = UserForm(request.POST, request=request)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('adminka'))  # Замените 'some_success_url' на нужный URL
    else:
        form = UserForm(request=request)

    return render(request, 'user-create.html', {'form': form})

@csrf_protect
def reader_create(request):

    if request.method == 'POST':
        form = ReaderForm(request.POST, request=request)
        if form.is_valid():
            reader = form.save()
            return redirect(reverse('index'))  
    else:
        form = ReaderForm(request=request)

    return render(request, 'reader-create.html', {'form': form})

@login_required(login_url="/login", redirect_field_name='continue')
def book(request, book_id):
    item = Book.objects.get(id=book_id)
    page_params=paginate(request, Rent.objects.all().filter(bookinstance__book__id=book_id))
    return render(request, "book.html", 
                    {'book': item,
                    'rents': page_params['content'], 
                   'genres': genres_all,
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})

@csrf_protect
def adminka(request):
    return render(request, 'admin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("login"))

@csrf_protect
def log_in(request):
    if request.user is not None:
        logout(request)
    if request.method=="GET":
        login_form=LoginForm()
    if request.method=="POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                if user.username=='admin':
                    login(request,user)
                    return redirect(reverse('adminka'))
                else:
                    login(request, user)
                    return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong password or user doesn't exist")
                login_form.add_error("password", "")
                login_form.add_error("username", "")

    return render(request, "login.html", context={"form": login_form})


def delete_rent_b(request, rent_id, book_id):
    object = Rent.objects.get(id=rent_id)
    object.delete()
    return redirect('book', book_id=book_id)

def delete_rent_r(request, rent_id, reader_id):
    object = Rent.objects.get(id=rent_id)
    object.delete()
    return redirect('reader', reader_id=reader_id)

def delete_reader(request, reader_id):
    object = Reader.objects.get(id=reader_id)
    object.delete()
    return redirect(reverse('readers'))

def delete_book(request, book_id):
    object = Book.objects.get(id=book_id)
    object.delete()
    return redirect(reverse('adminka'))

def delete_user(request, user_id):
    object = User.objects.get(id=user_id)
    object.delete()
    return redirect(reverse('adminka'))

@login_required(login_url="/login", redirect_field_name='continue')
def reader(request, reader_id):
    item = Reader.objects.get(id=reader_id)
    page_params=paginate(request, Rent.objects.all().filter(reader__id=reader_id))
    return render(request, "reader.html", 
                    {'reader': item,
                    'rents': page_params['content'], 
                   'genres': genres_all,
                   'page': page_params['page'], 
                   'prev_page': page_params['page']-1, 
                   'fol_page': page_params['page']+1,
                   'limit': page_params['limit']})