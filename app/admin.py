from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Member, Author, Category, Book, Borrow, Fine

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'contact')
    search_fields = ('name', 'course')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'quantity', 'isbn')
    list_filter = ('category', 'author')
    search_fields = ('title', 'isbn')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'borrow_date', 'due_date', 'status', 'is_overdue_check')
    list_filter = ('status', 'borrow_date')
    date_hierarchy = 'borrow_date' # Adds a timeline navigation at the top
    
    def is_overdue_check(self, obj):
        return obj.is_overdue
    is_overdue_check.boolean = True # Displays a green tick or red cross
    is_overdue_check.short_description = 'Overdue?'

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('borrow', 'amount', 'paid')
    list_filter = ('paid',)

admin.site.register(Author)
admin.site.register(Category)