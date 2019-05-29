from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import uploadFile
from django.core.files.storage import FileSystemStorage


def index(request):

    if request.method == 'POST' and request.FILES['myFile']:

        print ('This file = ' + str(request.FILES['myFile']))
        print ('This file = ' + str(request))

        myfile   = request.FILES['myFile']

        fs       = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # store uploaded file data in db
        upfile = uploadFile()
        upfile.name = filename

        # add path by if it's default or chosen file destination

        # save uploaded file
        upfile.save()

    #page template and view variables
    template = loader.get_template('upload/index.html')
    context = dict()


    return HttpResponse(template.render(context, request))