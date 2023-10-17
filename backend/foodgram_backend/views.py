from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'foodgram_backend/404.html', {
        'path': request.path
    }, status=404)
