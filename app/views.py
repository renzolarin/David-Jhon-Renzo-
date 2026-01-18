from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Borrow, Member, Author, Category
from django.utils import timezone
from datetime import timedelta

def home(request):
    context = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.count(),
        'active_borrows': Borrow.objects.filter(status='Borrowed').count(),
        # Adding recent transactions to the dashboard
        'recent_borrows': Borrow.objects.all().order_by('-id')[:5]
    }
    return render(request, 'app/home.html', context)

# --- NEW: ADD BOOK ---
def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            title=request.POST.get('title'),
            isbn=request.POST.get('isbn'),
            author_id=request.POST.get('author'),
            category_id=request.POST.get('category'),
            quantity=request.POST.get('quantity')
        )
        return redirect('book_list')
    
    authors = Author.objects.all()
    categories = Category.objects.all()
    return render(request, 'app/add_book.html', {'authors': authors, 'categories': categories})

# --- NEW: ISSUE BOOK ---
def issue_book(request):
    if request.method == "POST":
        book = get_object_or_404(Book, id=request.POST.get('book'))
        
        if book.quantity > 0:
            Borrow.objects.create(
                member_id=request.POST.get('member'),
                book=book,
                due_date=timezone.now().date() + timedelta(days=14),
                status='Borrowed'
            )
            # Reduce inventory
            book.quantity -= 1
            book.save()
            return redirect('home')
            
    books = Book.objects.filter(quantity__gt=0)
    members = Member.objects.all()
    return render(request, 'app/issue_book.html', {'books': books, 'members': members})

# --- NEW: RETURN BOOK ---
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if borrow.status == 'Borrowed':
        borrow.status = 'Returned'
        borrow.actual_return_date = timezone.now().date()
        borrow.save()

        # Add back to inventory
        borrow.book.quantity += 1
        borrow.book.save()
        
    return redirect('home')

# --- EXISTING VIEWS ---
def book_list(request):
    books = Book.objects.all()
    return render(request, 'app/catalog.html', {'books': books})

def borrow_list(request):
    borrows = Borrow.objects.all().order_by('-id')
    return render(request, 'app/issue_book.html', {'borrows': borrows})

def report_summary(request):
    active_borrows = Borrow.objects.filter(status='Borrowed')
    return render(request, 'app/reports.html', {'active_borrows': active_borrows})