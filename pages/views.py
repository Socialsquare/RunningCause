from django.shortcuts import render

def why_join_us(request):
    return render(request, 'pages/why_join_us.html')

def frontpage(request):
    return render(request, 'pages/frontpage.html')
