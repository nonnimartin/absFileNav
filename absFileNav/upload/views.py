from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import uploadFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import hashlib
from functools import partial
from util import createTree

def index(request):

    if request.method == 'POST' and request.FILES['myFile']:

        print ('This file = ' + str(request.FILES['myFile']))
        print ('This file = ' + str(request))

        myfile   = request.FILES['myFile']

        #if file is too big chunked will be true, and must be processed in stream
        chunked  = request.FILES['myFile'].multiple_chunks()
        print ('chunked = ' + str(chunked))

        if chunked:
            pass

        else:
            fs = FileSystemStorage()
            filename = fs.save(clean_file_name(myfile.name), myfile)
            uploaded_file_url = fs.url(filename)

            # store uploaded file data in db
            upfile = uploadFile()
            upfile.name = clean_file_name(filename)
            upfile.path = settings.MEDIA_ROOT

            upfile.checksum = hash_file(myfile.open())

            # add path by if it's default or chosen file destination

            # save uploaded file
            upfile.save()

    #page template and view variables
    template = loader.get_template('upload/index.html')

    #get json of file system for saving and set in view
    json_file_tree = createTree.path_hierarchy('.')

    context = dict()
    context['json_file_tree'] = createTree.path_hierarchy('.')


    return HttpResponse(template.render(context, request))

def replace_spaces(thisString):
    return thisString.replace(' ', '_')

def clean_file_name(fileName):
    thisString = replace_spaces(fileName)
    return thisString

def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()
