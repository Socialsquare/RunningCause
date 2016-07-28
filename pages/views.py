from django.shortcuts import render

def contact(request):
    return render(request, 'pages/contact.html')

def frontpage(request):
    return render(request, 'pages/frontpage.html')
