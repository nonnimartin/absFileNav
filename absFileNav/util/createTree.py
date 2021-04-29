import os
import json
import errno

path_to_id = {}
final_list = list()
rec_count = 0
recurse_children = list()


def path_hierarchy(path):

    # get file system represented as a hierarchy
    hierarchy = {
        'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
        print('child ' + str(hierarchy['children']))
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy


def recurse_tree(node_list, dirs_only):

    global path_to_id
    global final_list
    global rec_count
    global recurse_children

    # treat as list of nodes
    for item in node_list:

        # do not include files if dirs_only is true
        if dirs_only and item['type'] == 'file':
            continue
        # ignore hidden files
        if item['name'].startswith('.'):
            continue

        this_dict = dict()
        rec_count += 1
        this_dict['id'] = 'tree' + str(rec_count)
        if item['type'] == 'file':
            this_dict['icon'] = 'jstree-file'
        this_dict['type'] = item['type']
        this_dict['text'] = item['name']
        this_dict['fullPath'] = item['path']
        parent = item['path'].rsplit('/', 1)[0]

        if parent in path_to_id.keys():
            this_dict['parent'] = path_to_id[parent]
        else:
            this_dict['parent'] = '#'

        path_to_id[item['path']] = this_dict['id']

        final_list.append(this_dict)

        # handle children as new list
        if 'children' in item:
            recurse_tree(item['children'], dirs_only)

    return final_list


def get_tree(path, dirs_only):

    global path_to_id
    global final_list
    global rec_count
    global recurse_children
    hierarchy = path_hierarchy(path)
    hierarchy_list = [hierarchy]
    end_list = recurse_tree(hierarchy_list, False)

    # clear the globals
    path_to_id = {}
    final_list = list()
    rec_count = 0
    recurse_children = list()

    return json.dumps(end_list)
