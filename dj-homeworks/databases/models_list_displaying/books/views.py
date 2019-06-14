from django.shortcuts import render
from datetime import datetime
from .models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_pub_view(request, data):
    template = 'books/book_list.html'
    d = datetime.strptime(data, '%Y-%m-%d').date()
    prev_date = ''
    next_date = ''
    list_books = []
    books = Book.objects.order_by('pub_date')
    for book in books:
        if book.pub_date < d:
            prev_date = book.pub_date
        elif book.pub_date == d:
            list_books.append(book)
        elif book.pub_date > d:
            next_date = book.pub_date
            break
    context = {'books': list_books, 'prev_date': prev_date, 'next_date': next_date}
    return render(request, template, context)

