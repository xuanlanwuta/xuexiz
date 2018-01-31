from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from Book.models import BookInfo
# Create your views here.
def ajax(request):
    return render(request,'Book/ajax.html')

def jsondata(request):
    book_list = BookInfo.objects.all()
    book1 = []
    for book in book_list:
        book1.append({'name':book.name})
    print(book1)

    jsondict = {
        'jsondata':book1
    }
    return JsonResponse(jsondict)




def test(request,*args):
    str = "测试 tset----  %s" %args

    return HttpResponse(str)

def property(request):
    path = request.path
    methon = request.method
    query_dict = request.GET
    context={
        'path' : path,
        'methon':methon,
        'query_dict':query_dict
    }

    return render(request,"Book/property.html",context)

def get(request):


    return render(request,'Book/get.html')

def get1(request):
    str = (request.GET.get("a"),
    request.GET.get("b"),
    request.GET.get("c"))

    return HttpResponse(str)

def get2(request):
    return HttpResponse(request.GET.getlist("a") ,
                         request.GET.get("b") ,
                         )