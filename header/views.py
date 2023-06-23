from django.shortcuts import render, HttpResponse

# Create your views here.
def header(request):
    return render(request,"core/header.html")
