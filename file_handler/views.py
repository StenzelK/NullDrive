from django.contrib import messages
from django.shortcuts import render

from NullDrive import settings
from file_handler import list_files


# Create your views here.

def isIMG(f):
    if f.endswith("jpg") or f.endswith("png") or f.endswith("bmp") or f.endswith("gif") or f.endswith("jpeg"):
        return True
    return False


def handle_uploaded_file(f, username):
    with open('media/userfiles/{}/{}'.format(username, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def files(request):
    if request.user.is_authenticated:
        username = request.user.username


        if request.method == 'POST':

            if 'filename' in request.POST:

                filename = request.POST['filename']

                messages.info(request, "Deleted {}".format(filename))

                list_files.secure_delete(username, filename)

            else:
                for f in request.FILES.getlist("upload"):

                    handle_uploaded_file(f, username)
                    if list_files.check_dir_size(('media/userfiles/{}'.format(username))):
                        messages.info(request, "Uploaded file {}".format(f))
                    else:
                        messages.error(request, "Not enough space")
                        list_files.secure_delete(username, f.name)

        filelist = list_files.list_files(username)


        dir_size = list_files.get_dir_size('media/userfiles/{}'.format(username))
        images = [file for file in filelist if isIMG(file)]
        other = [file for file in filelist if file not in images]

        return render(request=request,
                      template_name='file_handler/index.html',
                      context={"username": username,
                               "images": images,
                               "other": other,
                               "dir_size": dir_size})

    else:
        return render(request=request,
                      template_name='main/login.html', )
