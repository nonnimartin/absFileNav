from django.http import HttpResponse

# from django.shortcuts import render
from django.template import loader
from .models import uploadFile
from .models import UserSettings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import hashlib
from functools import partial
from util import createTree
from forms import FileUploadPath
import json
import os, errno

# chunked uploads library imports

from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.utils import timezone

from .settings import MAX_BYTES
from .models import ChunkedUpload
from .response import Response
from .constants import http_status, COMPLETE
from .exceptions import ChunkedUploadError

# make sure this import is needed
from upload.upload_forms import SettingsForm

from django.shortcuts import redirect
from django.utils import timezone

def new_path(request):
    if request.method == 'POST':
        body_string = request.body
        body        = json.loads(body_string.decode('utf-8'))
        new_path = body['newPath']

        #write new directory to file system
        new_dir = create_dir(new_path)

        if new_dir:
            return HttpResponse({'success'}, content_type='application/json')
        else:
            failure_response = HttpResponse()
            failure_response.status_code = 500
            return failure_response
    else:
        return HttpResponse('{}', content_type='application/json')

def delete_path(request):
    if request.method == 'POST':
        body_string = request.body
        body        = json.loads(body_string)
        delete_path = body['delete_path']

        #write new directory to file system
        #delete_path = create_dir(delete_path)

        if new_dir:
            return HttpResponse({'success'}, content_type='application/json')
        else:
            failure_response = HttpResponse()
            failure_response.status_code = 500
            return failure_response
    else:
        return HttpResponse('{}', content_type='application/json')


def index(request):

    if request.method == 'POST' and request.FILES['myFile']:

        this_form = FileUploadPath(request.POST)
        files_list = request.FILES.getlist('myFile')

        #initialize path variable
        path = False

        # check whether it's valid:
        if this_form.is_valid():
            path = this_form.cleaned_data['path']

        for this_file in files_list:

            print('this file = ' + str(this_file))

            try:

                if path:
                    # store uploaded file data in db
                    upfile = uploadFile()
                    upfile.name = str(this_file)
                    upfile.path = path
                else:
                    # save file on hard drive on setting FILE_SYSTEM_ROOT
                    # should eventually be configurable

                    path = settings.MEDIA_ROOT

                    fs = FileSystemStorage(settings.FILE_SYSTEM_ROOT)
                    filename = fs.save(clean_file_name(this_file.name), this_file)

                    # store uploaded file data in db
                    upfile = uploadFile()
                    upfile.name = clean_file_name(filename)
                    # this should eventually be configurable
                    upfile.path = path

                newPath = str(path) + '/' + str(replace_spaces(this_file.name))
                print('Writing to path: ' + newPath)

                #open and write file
                with open(newPath, 'wb+') as destination:
                    for chunk in this_file.chunks():
                        destination.write(chunk)

                destination.close()

            except Exception as e:
                # get error message
                print('Error writing file: ' + str(e))
                payload = {'success': False, 'error': str(e)}
                return HttpResponse(json.dumps(payload), content_type='application/json')


            upfile.checksum = hash_file(this_file.open())
            # save uploaded file
            upfile.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')

    #file upload path form
    pathForm = FileUploadPath()

    #page template and view variables
    template = loader.get_template('upload/index.html')

    #get json of file system for saving and set in view
    context = dict()
    context['path_selected']  = False
    context['form'] = pathForm
    context['json_file_tree'] = createTree.get_tree(settings.FILE_SYSTEM_ROOT, True)


    return HttpResponse(template.render(context, request))

def user_settings(request):

    stored_settings     = UserSettings.objects.all()
    has_stored_settings = True if len(stored_settings) > 0 else False

    if request.method == 'POST':

        base_folder = str()
        show_files  = bool()

        base_folder = request.POST['base_folder']
        if 'show_files' in request.POST.keys():
            show_files = request.POST['show_files']
            print('show files in here ' + show_files)
            if show_files == 'on':
                show_files = True

        print('post base folder = ' + base_folder)

        save_settings = UserSettings()
        save_settings.id = 1
        save_settings.show_files  = show_files
        save_settings.base_folder = base_folder
        save_settings.last_modified = timezone.now()
        print('save settings show files = ' + str(save_settings.show_files))

        try:
            save_settings.save()
            return redirect('/upload/')
        except Exception as e:
            print('Error saving settings: ' + str(e))

    user_settings = SettingsForm()
    context         = dict()

    if has_stored_settings:
        #if has stored settings, retrieve them
        stored_settings               = stored_settings[0]
        context['base_folder']        = stored_settings.base_folder
        print('show files ' + str(stored_settings.show_files))
        context['show_files']         = stored_settings.show_files
    else:
        context['show_files']  = False

    context['json_file_tree'] = createTree.get_tree(settings.FILE_SYSTEM_ROOT, True)
    context['form'] = user_settings
    template = loader.get_template('user_settings/index.html')
    return HttpResponse(template.render(context, request))

def replace_spaces(this_string):
    return this_string.replace(' ', '_')

def clean_file_name(file_name):
    thisString = replace_spaces(file_name)
    return thisString

def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
        return True
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def delete_path(path):
    #add logic for deleting files/dirs carefully
    print('delete path = ' + path)

def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()
