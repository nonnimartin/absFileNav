import os
import json
import errno

path_to_id = {}

def path_hierarchy(path):
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
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy


def recurse_children(child_list, counter):
    # recurse children until no more children to recurse

    this_dict = dict()
    return_list = list()

    #print('this map = ' + str(path_to_id))

    for node in child_list:
        print('this node processing: ' + str(node))
        counter += 1
        print('counter = ' + str(counter))
        this_dict['id'] = 'tree' + str(counter)
        path_to_id[node['path']] = this_dict['id']
        this_dict['text'] = node['name']
        this_dict['type'] = node['type']
        this_path = node['path'].rsplit('/', 1)[0]
        print('this path = ' + this_path)
        this_dict['parent'] = path_to_id[this_path]

        print('this node finished: ' + str(this_dict))
        print('=======================================')

        #THIS WILL NOT HANDLE ALL CHILDREN
        ##MAYBE GO THROUGH SERIALLY AND POP ITEMS?
        if 'children' in node:
            recurse_children(node['children'], counter)

        return_list.append(this_dict)

    return return_list


def prepare_for_tree_view(dir_dict):
    counter = 0
    tree_list = list()
    returned_children = list()

    # print(json.dumps(dir_dict))

    # create base dir entry
    print('this node processing: ' + str(dir_dict))
    this_dict = dict()
    this_dict['id'] = 'tree' + str(counter)
    this_dict['parent'] = '#'
    this_dict['type'] = dir_dict['type']
    this_dict['text'] = dir_dict['name']
    print(this_dict)
    tree_list.append(this_dict)

    # map path to unique id
    path_to_id[dir_dict['path']] = this_dict['id']

    # if there are children, recurse through them and their children and create entries
    # RECURSE IN HERE
    if 'children' in dir_dict:
        children = dir_dict['children']
        returned_children = recurse_children(children, counter)

    tree_list = tree_list + returned_children

    return tree_list


def main():
    testThis = path_hierarchy('/tmp/test')
    return json.dumps(prepare_for_tree_view(testThis))


if __name__ == '__main__':
    main()