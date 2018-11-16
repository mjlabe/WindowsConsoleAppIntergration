import os
import subprocess
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ConsoleAppIntegration.settings import STATIC_ROOT


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        uploaded_file_path = fs.path(filename)
        filename_noext = os.path.splitext(filename)[0]
        filepath = os.path.dirname(uploaded_file_path) + "\\"

        app = STATIC_ROOT + "\\ConsoleApplication.exe"
        p = subprocess.Popen([str(app)], stdin=subprocess.PIPE)

        command1 = "1" + "\n"
        command2 = uploaded_file_path + "\n"
        command3 = "2" + "\n"
        command4 = filepath + "result_" + filename_noext + ".doc" + "\n"
        command5 = "z" + "\n"

        # issue commands...
        p.stdin.write(command1.encode('utf-8'))
        p.stdin.write(command2.encode('utf-8'))
        p.stdin.write(command3.encode('utf-8'))
        p.stdin.write(command4.encode('utf-8'))
        p.stdin.write(command5.encode('utf-8'))

        p.stdin.close()

        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def wdir(dir):
    dir.replace('\\\\', '\\')
    return dir
