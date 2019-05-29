from django.http import HttpResponse
from django.template import loader
from .models import uploadFile


def index(request):

    template = loader.get_template('upload/index.html')
    context = dict()
    return HttpResponse(template.render(context, request))