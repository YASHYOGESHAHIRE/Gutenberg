
from django.contrib import admin
from django.urls import path
from .views import BookListAPIView, autofill_books, debug_books, fix_books
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/autofill/', autofill_books, name='book-autofill'),
    path('books/debug/', debug_books, name='book-debug'),
    path('books/fix/', fix_books, name='book-fix'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
