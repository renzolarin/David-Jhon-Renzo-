from django.db import models
from django.utils import timezone
from datetime import timedelta

class Member(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories" # Fixes 'Categorys' typo in Admin

    def __str__(self):
        return self.category_name

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True) # Prevent duplicate ISBNs
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) # Cannot be negative

    def __str__(self):
        return self.title

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True) # Automatically set to today
    due_date = models.DateField() # Set manually or via logic
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Borrowed')

    @property
    def is_overdue(self):
        """Returns True if book is not returned and today is past due date"""
        if self.status == 'Borrowed' and timezone.now().date() > self.due_date:
            return True
        return False

    def __str__(self):
        return f"{self.member.name} - {self.book.title}"

class Fine(models.Model):
    borrow = models.OneToOneField(Borrow, on_delete=models.CASCADE, related_name='fine')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine: {self.amount} for {self.borrow}"