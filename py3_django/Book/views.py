from django.shortcuts import render
from Book.models import BookInfo,PeopleInfo
# Create your views here.


def index(request):
    context = {'test': "测试版"}
    return render(request,'book/index.html',context)

def bookhtml(request):
    book_list = BookInfo.objects.all()
    context = {
        'book_list' : book_list
    }
    return render(request,'book/book.html',context)

def renwu(request,book_id):
    renwu = BookInfo.objects.get (id=book_id)
    renwu_list = renwu.peopleinfo_set.all()
    context = {
        'renwu_list': renwu_list
    }
    return render(request,'book/renwu.html',context)