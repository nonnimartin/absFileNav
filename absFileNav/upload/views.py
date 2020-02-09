from django.http import HttpResponse
from django.shortcuts import render
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
from upload.upload_forms import SettingsForm
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.files.storage import default_storage
import sys
from shutil import rmtree

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

    # check for stored settings
    stored_settings     = UserSettings.objects.all()
    has_stored_settings = True if len(stored_settings) > 0 else False

    if request.method == 'POST' and request.FILES['myFile']:

        this_form = FileUploadPath(request.POST)
        files_list = request.FILES.getlist('myFile')

        #initialize path variable
        path = False

        # check whether it's valid:
        if this_form.is_valid():
            path = this_form.cleaned_data['path']

        for this_file in files_list:

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
    path_form = FileUploadPath()

    #page template and view variables
    template = loader.get_template('upload/index.html')

    #get json of file system for saving and set in view
    context = dict()
    context['path_selected']  = False
    context['form'] = path_form
    if has_stored_settings:
        context['base_folder'] = str(stored_settings[0].base_folder)
    context['json_file_tree'] = createTree.get_tree(settings.FILE_SYSTEM_ROOT, True)


    return HttpResponse(template.render(context, request))

def clear_base_folder(request):
    settings  = UserSettings.objects.get(id=1)

    try:
        settings.base_folder = ''
        settings.save()
        return HttpResponse('SUCCESS')
    except Exception as error:
        print('Error writing to database: ' + str(error))
        return HttpResponse('FAILURE')

def delete_file(file_path):
    os.remove(file_path)

def user_settings(request):

    user_settings    = SettingsForm()
    background_image_location = settings.MEDIA_ROOT
    stored_settings     = UserSettings.objects.all()
    has_stored_settings = True if len(stored_settings) > 0 else False

    if request.method == 'POST':

        base_folder      = request.POST['base_folder']

        save_settings = UserSettings()
        save_settings.id = 1
        save_settings.base_folder      = base_folder
        save_settings.last_modified    = timezone.now()

        if 'background_image' not in request.FILES.keys():
            background_image_post_name = str() 
        else:
            background_image_post      = request.FILES['background_image']
            background_image_post_name = background_image_post.name

        # if saving background image
        if len(background_image_post_name) > 0:
            # write background image to background image location
            try:
                # list files in background image directory
                background_dirs_list = os.listdir(background_image_location)

                # delete files in background image directory
                for this_file in background_dirs_list:
                    delete_file(background_image_location + '/' + this_file)

                # open file at destination as binary appending
                write_bg_image = open(background_image_location + '/' + background_image_post.name, 'ab')

                for chunk in background_image_post.chunks():
                    write_bg_image.write(chunk)
                    # save location of background image to database
                    save_settings.background_image = background_image_location + '/' + background_image_post.name
            
                write_bg_image.close()
            except Exception as e:
                print('Error saving settings: ' + str(e))
                print('Exception type 1 : ' + str(sys.exc_info()[0]))

        try:
            save_settings.save()
            return redirect('/upload/')
        except Exception as e:
            print('Error saving settings: ' + str(e))
            print('Exception type 2: ' + str(sys.exc_info()[0]))

    context          = dict()

    if has_stored_settings:
        #if has stored settings, retrieve them
        stored_settings               = stored_settings[0]
        context['base_folder']        = stored_settings.base_folder
        context['show_files']         = stored_settings.show_files
        context['background_image']   = stored_settings.background_image
        context['background_image']   = stored_settings.background_image
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

def delete_dir_recursively(dir_path):
    try:
        rmtree(dir_path)
        return True
    except:
        print('Exception type : ' + str(sys.exc_info()[0]))

def dir_exists(dir_path):
    return os.path.exists(dir_path)

# store a map of each unique file id and an int for how many more bytes it needs
chunks_map = dict()
path_map   = dict()

def register_chunk(tmp_file_name, file_size, current_size):
    chunks_map[tmp_file_name] = file_size - current_size

def reduce_file_size(tmp_file_name, current_size):
    chunks_map[tmp_file_name] = chunks_map[tmp_file_name] - current_size

def get_file_size(tmp_file_name):
    return chunks_map[tmp_file_name]

def concatenate_files(file_name, destination_dir, file_tmp_dir, total_chunks, destination):
    
    files_map = dict()
    list_dir  = os.listdir(file_tmp_dir) 

    # get list of numbers between 0 and total_chunks
    chunks_list = list(list(range(1, total_chunks + 1)))
    
    # construct mapping of numbers to files, organizing files into ordered listing
    for item in list_dir:
        files_map[int(item.split('TMPFILE-')[1])] = item
    
    try:
        # open file at destination as binary appending
        write_file = open(destination, 'ab')

        write_file_path = destination_dir + '/' + file_name

        # write each file to the end of the file at destination location
        write_file  = open(write_file_path, 'ab')

        for chunk_num in chunks_list:
            # read file of this num
            read_file_name  = file_tmp_dir + files_map[chunk_num]

            # open partial file to read each iteration
            with open(read_file_name, mode='rb') as read_file:
                binary_data = read_file.read()

                # write partial file to single destination file
                write_file.write(binary_data)
                read_file.close()
        write_file.close()
        delete_dir_recursively(file_tmp_dir)
    
    except:
        print('Exception type : ' + str(sys.exc_info()[0]))
        print('Exception info : ' + str(sys.exc_info()[3]))


def delete_keys(tmp_file_name):
    del chunks_map[tmp_file_name]

def receive_resumable(request):

    if request.method == 'POST':
        this_file        = request.FILES['file']
        file_name        = this_file.name
        destination_dir  = str(request.headers['destination'])
        destination_path = destination_dir + '/' + this_file.name
        chunk_size       = str(request.POST.get('resumableChunkSize'))
        chunk_num        = int(request.POST.get('resumableChunkNumber'))
        file_total_size  = int(request.POST.get('resumableTotalSize'))
        current_size     = int(request.POST.get('resumableCurrentChunkSize'))
        total_chunks     = int(request.POST.get('resumableTotalChunks'))
        file_root_name   = this_file.name + '-TMPFILE-'
        tmp_file_name    = file_root_name +  str(chunk_num)
        tmp_dir          = destination_dir + '/tmp-TMPDIR-' + this_file.name + '/'
        tmp_dest         = tmp_dir + tmp_file_name

        try:
            if not dir_exists(tmp_dir):
                # if local tmp dir doesn't exist, make it so
                create_dir(tmp_dir)
        except:
            print('Exception type : ' + str(sys.exc_info()[0]))
            print('Exception info : ' + str(sys.exc_info()[3]))
            return HttpResponse(status=500)

        try:
            with default_storage.open(tmp_dest, 'ab') as destination:

                for chunk in this_file.chunks():
                    destination.write(chunk)
                
            if file_root_name not in chunks_map.keys():
                # add tmp file name if not in map
                register_chunk(file_root_name, file_total_size, current_size)
            else:
                # reduce total size remaining in map
                reduce_file_size(file_root_name, current_size)
            
            # if size of remaining chunks is 0
            if get_file_size(file_root_name) == 0:
                # concatenate file pieces and write to a single file
                concatenate_files(file_name, destination_dir, tmp_dir, total_chunks, destination_path)
                #clear maps from memory to avoid memory leak
                delete_keys(file_root_name)
            
            return HttpResponse(status=200)
        except:
            print('Exception type : ' + str(sys.exc_info()[0]))
            print('Exception type : ' + str(sys.exc_info()[3]))
            return HttpResponse(status=500)
    elif request.method == 'GET':
        return HttpResponse(status=202)
