from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import uploadFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import hashlib
from functools import partial
from util import createTree
from forms import FileUploadPath

def index(request):

    #print('content_params = ' + str(form))

    if request.method == 'POST' and request.FILES['myFile']:

        this_form = FileUploadPath(request.POST)

        #initialize path variable
        path = False

        # check whether it's valid:
        if this_form.is_valid():
            path = this_form.cleaned_data['path']

        myfile   = request.FILES['myFile']

        #if file is too big chunked will be true, and must be processed in stream
        chunked  = request.FILES['myFile'].multiple_chunks()

        if chunked:
            #handle larger file streams here
            print('got here')
            pass

        else:
            if path:
                #save file on hard drive
                fs = FileSystemStorage(path)
                filename = fs.save(clean_file_name(myfile.name), myfile)

                # store uploaded file data in db
                upfile = uploadFile()
                upfile.name = clean_file_name(filename)
                upfile.path = path
            else:
                #save file on hard drive on setting media root
                #should eventually be configurable
                fs = FileSystemStorage(settings.MEDIA_ROOT)

                filename = fs.save(clean_file_name(myfile.name), myfile)

                # store uploaded file data in db
                upfile = uploadFile()
                upfile.name = clean_file_name(filename)
                #this should eventually be configurable
                upfile.path = settings.MEDIA_ROOT

            upfile.checksum = hash_file(myfile.open())
            # save uploaded file
            upfile.save()

    #file upload path form
    pathForm = FileUploadPath()

    #page template and view variables
    template = loader.get_template('upload/index.html')

    #get json of file system for saving and set in view
    context = dict()
    context['path_selected']  = False
    context['form'] = pathForm
    context['json_file_tree'] = createTree.get_tree('/Users/jonathanmartin/Desktop', True)


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
