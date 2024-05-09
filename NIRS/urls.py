"""
URL configuration for NIRS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login', views.log_in, name='login'),
    path('book/<int:book_id>', views.book, name='book'),
    path('rent_create', views.rent_create, name='rent_create'),
    path('book_create', views.book_create, name='book_create'),
    path('reader_create', views.reader_create, name='reader_create'),
    path('reader/<int:reader_id>', views.reader, name='reader'),
    path('books', views.books, name='books'),
    path('readers', views.readers, name='readers'),
    path('genres/<str:genre_name>', views.genres, name='genres'),
    path('delete_rent_b/<str:rent_id>/<str:book_id>', views.delete_rent_b, name='delete_rent_b'),
    path('delete_rent_r/<str:rent_id>/<str:reader_id>', views.delete_rent_r, name='delete_rent_r'),
    path('delete_reader/<str:reader_id>', views.delete_reader, name='delete_reader'),
    path('adminka', views.adminka, name='adminka'),
    path('books_adminka', views.books_adminka, name='books_adminka'),
    path('users', views.users, name='users'),
    path('delete_book/<str:book_id>',views.delete_book, name='delete_book'),
    path('delete_user/<str:user_id>',views.delete_user, name='delete_user'),
    path('user_create', views.user_create, name='user_create')
]
