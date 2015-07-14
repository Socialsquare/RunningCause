from django.shortcuts import render


def why_join_us(request):
    ctx = {}
    return render(request, 'pages/why_join_us.html', ctx)
