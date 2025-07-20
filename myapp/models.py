from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Subject(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Bookshelf(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    subjects = models.ManyToManyField(Subject)
    bookshelves =models.ManyToManyField(Bookshelf)
    language =models.CharField(max_length=10)
    download_count = models.IntegerField(default=0)
    format = models.CharField(max_length=100, blank=True, null=True)
    download_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
class Format(models.Model):
    FORMAT_CHOICES = [
    ('application/pdf', 'PDF'),
    ('text/plain', 'Text'),
    ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'DOCX'),
    ('application/epub+zip', 'EPUB'),
    ]

    book=models.ForeignKey(Book,related_name='formats', on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='formats/', null=True, blank=True)
    mime_type=models.CharField(max_length=100,choices=FORMAT_CHOICES)
    url=models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.mime_type} of {self.book.title}"