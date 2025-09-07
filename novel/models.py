from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    website = models.URLField(max_length=2085)
    established_year = models.IntegerField(null=True, blank=True)  # Kab publisher start hua
    contact_number = models.CharField(max_length=15, null=True, blank=True)  # Phone number
    is_active = models.BooleanField(default=True)  # Publisher active hai ya nahi

    def __str__(self):
        return f'{self.id}' 

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    bio = models.TextField(max_length=500, null=True, blank=True)  # Author ki details
    birth_date = models.DateField(null=True, blank=True)  # DOB
    profile_picture = models.ImageField(upload_to='author_pics/', null=True, blank=True)  # Author ki photo

    def __str__(self):
        return self.first_name
    


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher_id = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)  # ISBN number
    genre = models.CharField(max_length=50, null=True, blank=True)  # Fiction, non-fiction, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Book ka price
    pages = models.IntegerField(null=True, blank=True)  # Total pages
    language = models.CharField(max_length=30, null=True, blank=True)  # Book ki language
    stock_quantity = models.IntegerField(default=0)  # Available copies
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # Book ka cover



















