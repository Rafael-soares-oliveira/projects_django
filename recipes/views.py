from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'nivel1/home.html')


def about(request):
    return render(request, 'nivel1/about.html')


def contact(request):
    return render(request, 'nivel1/contact.html')
