from rest_framework import serializers
from .models import Author ,Subject,Bookshelf, Book, Format

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields=['name']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    subjects = serializers.StringRelatedField(many=True)
    bookshelves = serializers.StringRelatedField(many=True)
    formats = FormatSerializer(many=True, read_only=True)
    download_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'subjects', 'bookshelves', 'formats', 'language', 'download_count', 'download_link']
    
    def get_download_link(self, obj):
        request = self.context.get('request')
        
        # First, try to find a format with an uploaded file (PDF)
        format_with_file = obj.formats.filter(uploaded_file__isnull=False).first()
        if format_with_file and format_with_file.uploaded_file:
            return request.build_absolute_uri(format_with_file.uploaded_file.url)
        
        format_with_url = obj.formats.filter(url__isnull=False).first()
        if format_with_url and format_with_url.url:
            return format_with_url.url
        
        return None