from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.book_list, name='book_list'),
    path('borrow/', views.borrow_list, name='borrow_list'),
    path('reports/', views.report_summary, name='reports'),
    path('add-book/', views.add_book, name='add_book'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/<int:borrow_id>/', views.return_book, name='return_book'),
]