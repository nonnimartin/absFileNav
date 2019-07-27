# absFileNav
Must set ALLOWED_HOSTS in settings.py to hostname when deployed

Must set port with runserver when deployed

Depends on Chunked File Upload: https://pypi.org/project/django-chunked-upload/
- Run `pip3 install django-chunked-upload
- Itself depends on https://github.com/blueimp/jQuery-File-Upload
- This will need installing virtualenv with `git clone git@github.com:juliomalegria/django-chunked-upload-demo.git`

Followed by:

`virtualenv ven`
`source venv/bin/activate`
`pip3 install -r requirements.txt`
`./manage.py syncdb --noinput`
