from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-download_count')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = None  # We will add custom pagination in settings or here

    filterset_fields = {
        'id': ['exact', 'in'],
        'language': ['exact', 'in'],
        'formats__mime_type': ['icontains'],
        'authors__name': ['icontains'],
        'title': ['icontains'],
        'subjects__name': ['icontains'],
        'bookshelves__name': ['icontains'],
    }

    search_fields = [
        'title',
        'authors__name',
        'subjects__name',
        'bookshelves__name',
    ]


from django.http import JsonResponse
from .models import Book, Author, Subject, Bookshelf,Format
import random


from faker import Faker
fake = Faker()
import os
from django.core.files import File
from django.conf import settings

def autofill_books(request):
    mime_types = [
        'application/pdf',
        'text/plain',
        'application/epub+zip',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]

    for i in range(20):
        author, _ = Author.objects.get_or_create(name=fake.name())
        subject, _ = Subject.objects.get_or_create(name=fake.word())
        bookshelf, _ = Bookshelf.objects.get_or_create(name=fake.word())

        mime = random.choice(mime_types)
        download_url = fake.url()

        book = Book.objects.create(
            title=fake.sentence(nb_words=5),
            language=random.choice(['en', 'fr', 'de', 'es']),
            download_count=random.randint(0, 1000),
            download_link=download_url,
            format=mime
        )
        book.authors.add(author)
        book.subjects.add(subject)
        book.bookshelves.add(bookshelf)

        if i < 5:
            sample_pdf_path = os.path.join(settings.MEDIA_ROOT, 'sample.pdf')
            if os.path.exists(sample_pdf_path):
                with open(sample_pdf_path, 'rb') as f:
                    django_file = File(f, name=f'sample_{i}.pdf')
                    Format.objects.create(
                        book=book,
                        mime_type='application/pdf',
                        uploaded_file=django_file,
                        url=None
                    )
            else:
                return JsonResponse({'error': f'Sample PDF not found at {sample_pdf_path}'})
        else:
            Format.objects.create(
                book=book,
                mime_type=mime,
                uploaded_file=None,
                url=download_url
            )

    return JsonResponse({"message": "20 books created. 5 with real PDF uploads!"})


def debug_books(request):
    """Debug view to check the current state of books and formats"""
    books_data = []
    for book in Book.objects.all()[:5]:  
        formats_data = []
        for format_obj in book.formats.all():
            formats_data.append({
                'id': format_obj.id,
                'mime_type': format_obj.mime_type,
                'has_uploaded_file': bool(format_obj.uploaded_file),
                'uploaded_file_url': format_obj.uploaded_file.url if format_obj.uploaded_file else None,
                'has_url': bool(format_obj.url),
                'url': format_obj.url
            })
        
        books_data.append({
            'id': book.id,
            'title': book.title,
            'formats_count': book.formats.count(),
            'formats': formats_data
        })
    
    return JsonResponse({'books': books_data})


def fix_books(request):
    """Fix existing books by adding uploaded PDF files to formats that don't have them"""
    sample_pdf_path = os.path.join(settings.MEDIA_ROOT, 'sample.pdf')
    
    if not os.path.exists(sample_pdf_path):
        return JsonResponse({'error': f'Sample PDF not found at {sample_pdf_path}'})
    
    fixed_count = 0
    for book in Book.objects.all():
        has_uploaded_file = book.formats.filter(uploaded_file__isnull=False).exists()
        
        if not has_uploaded_file:
            pdf_format = book.formats.filter(mime_type='application/pdf').first()
            
            if pdf_format:
                with open(sample_pdf_path, 'rb') as f:
                    django_file = File(f, name=f'sample_fixed_{book.id}.pdf')
                    pdf_format.uploaded_file = django_file
                    pdf_format.save()
            else:
                with open(sample_pdf_path, 'rb') as f:
                    django_file = File(f, name=f'sample_new_{book.id}.pdf')
                    Format.objects.create(
                        book=book,
                        mime_type='application/pdf',
                        uploaded_file=django_file,
                        url=None
                    )
            fixed_count += 1
    
    return JsonResponse({
        "message": f"Fixed {fixed_count} books with uploaded PDF files",
        "fixed_count": fixed_count
    })
