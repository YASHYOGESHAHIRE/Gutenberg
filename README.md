# 📚 Gutenberg Book API

A comprehensive Django REST Framework (DRF) project that provides a public API to query and retrieve books from Project Gutenberg. The API supports flexible filtering, pagination, and downloadable book formats, with sorting based on popularity.

<img width="1168" height="870" alt="Screenshot 2025-07-20 110326" src="https://github.com/user-attachments/assets/c8e24415-213e-42df-b3c2-f7827681de4c" />
<img width="717" height="801" alt="Screenshot 2025-07-20 110342" src="https://github.com/user-attachments/assets/cdd6571a-a354-4701-9699-3aed3f7ce4a9" />

## 🌟 Features

### 🔍 Advanced Filtering Options
- **Project Gutenberg ID**: Filter by specific book IDs
- **Language**: Support for multiple languages (e.g., `en`, `fr`, `es`)
- **Title**: Case-insensitive partial matching
- **Author**: Search by author name (case-insensitive)
- **Subject**: Filter by book subjects
- **Bookshelf**: Filter by Project Gutenberg bookshelves
- **MIME Type**: Filter by available formats (`application/pdf`, `text/html`, etc.)

### ⚡ Additional Features
- **Multiple Values**: Support for comma-separated filter values
- **Pagination**: Clean pagination with 20 results per page
- **Popularity Sorting**: Results sorted by download count
- **Download Links**: Direct access to book files in various formats
- **RESTful Design**: Clean JSON responses following REST principles

## 📸 Screenshots

### API Response Example
```json
{
  "id": 158,
  "title": "close experience represent ability decade family.",
  "authors": [
    {
      "name": "Timothy More"
    }
  ],
  "subjects": [
    "music"
  ],
  "bookshelves": [
    "everybody"
  ],
  "formats": [
    {
      "mime_type": "application/pdf"
    }
  ],
  "language": "es",
  "download_count": 564,
  "download_link": "http://127.0.0.1:8000/media/formats/sample_3_kQ7l51q.pdf"
}
```

### Advanced Filtering Interface
The API provides a comprehensive filtering system with support for:
- Field-specific filters
- Multi-value filtering with comma separation
- Full-text search capabilities
- MIME type filtering for format-specific queries

## 🛠 Tech Stack

- **Backend Framework**: Django 5.x
- **API Framework**: Django REST Framework
- **Database**: MySQL
- **Authentication**: Django's built-in authentication system

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/gutenberg-api.git
cd gutenberg-api
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Linux/macOS:
source env/bin/activate
# On Windows:
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💾 Database Setup

### MySQL Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server mysql-client
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### macOS (with Homebrew)
```bash
brew install mysql
brew services start mysql
```

#### Windows
Download and install from: https://dev.mysql.com/downloads/installer/

### Database Configuration

1. **Access MySQL shell**:
```bash
mysql -u root -p
```

2. **Create database and user**:
```sql
CREATE DATABASE gutenberg CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'gutenberg_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON gutenberg.* TO 'gutenberg_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

3. **Configure Django settings** (`settings.py`):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gutenberg',
        'USER': 'gutenberg_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### Django Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## 🎯 API Usage

### Base Endpoint
```
http://127.0.0.1:8000/api/books/
```

### HTTP Methods Supported
- `GET`: Retrieve books list
- `HEAD`: Get response headers
- `OPTIONS`: Get allowed methods and field information

### Content Type
- **Response**: `application/json`
- **Request**: Supports query parameters

## 📌 API Examples

### Basic Queries

**Get all books:**
```bash
GET /api/books/
```

**Get books by language:**
```bash
GET /api/books/?language=en
```

**Search by author:**
```bash
GET /api/books/?authors=Timothy More
```

**Filter by title:**
```bash
GET /api/books/?title=experience
```

**Filter by subject:**
```bash
GET /api/books/?subjects=music
```

**Filter by bookshelf:**
```bash
GET /api/books/?bookshelves=everybody
```

**Filter by MIME type:**
```bash
GET /api/books/?formats=application/pdf
```

### Advanced Queries

**Multiple languages:**
```bash
GET /api/books/?language=en,fr,es
```

**Multiple authors:**
```bash
GET /api/books/?authors=Timothy More,Jacqueline Smith
```

**Combined filters:**
```bash
GET /api/books/?language=en&subjects=music&formats=application/pdf
```

**Pagination:**
```bash
GET /api/books/?page=2
```

**Complex search:**
```bash
GET /api/books/?language=en,fr&subjects=music,water&title=program
```

## 📊 Response Format

### Success Response (200 OK)
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 158,
      "title": "close experience represent ability decade family.",
      "authors": [
        {
          "name": "Timothy More"
        }
      ],
      "subjects": ["music"],
      "bookshelves": ["everybody"],
      "formats": [
        {
          "mime_type": "application/pdf"
        }
      ],
      "language": "es",
      "download_count": 564,
      "download_link": "http://127.0.0.1:8000/media/formats/sample_3_kQ7l51q.pdf"
    }
  ]
}
```

### Field Descriptions
- **id**: Project Gutenberg book ID
- **title**: Book title
- **authors**: Array of author objects with names
- **subjects**: Array of subject categories
- **bookshelves**: Array of Project Gutenberg bookshelf categories
- **formats**: Array of available format objects
- **language**: Two-letter language code
- **download_count**: Number of downloads (used for sorting)
- **download_link**: Direct download URL for the book

## 🔧 Development

### Adding Sample Data

1. **Access Django Admin**:
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Add data in this order**:
   - Authors
   - Subjects
   - Bookshelves
   - Books (link to authors, subjects, bookshelves)
   - Formats (link to books)

### Project Structure
```
gutenberg-api/
├── manage.py
├── requirements.txt
├── gutenberg_api/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── static/
    └── media/
```



**Made with ❤️ using Django REST Framework**
