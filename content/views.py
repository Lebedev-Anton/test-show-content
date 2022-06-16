"""Views для приложения content."""
from content.services.chooser.ChoosePhoto import get_next_url

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """View для отображения изображений."""
    categories = request.GET.getlist('category')
    url_pic = get_next_url(categories)
    return render(request, 'index.html', {'url_pic': url_pic})
