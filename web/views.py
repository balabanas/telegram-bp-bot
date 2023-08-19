from django.shortcuts import render


def start(request):
    return render(request, 'web/start.html')
