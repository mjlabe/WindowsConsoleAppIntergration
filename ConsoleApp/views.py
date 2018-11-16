import os
import subprocess
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import smart_str

from ConsoleAppIntegration.settings import STATIC_ROOT


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_path = fs.path(filename)
        filename_out = "result_" + os.path.splitext(filename)[0] + ".doc"
        filepath = os.path.dirname(uploaded_file_path) + "\\"

        app = STATIC_ROOT + "\\ConsoleApplication.exe"
        p = subprocess.Popen([str(app)], stdin=subprocess.PIPE)

        # Commands to send
        commands = []
        commands.append("1" + "\n")
        commands.append(uploaded_file_path + "\n")
        commands.append("2" + "\n")
        commands.append(filepath + filename_out + "\n")
        commands.append("z" + "\n")

        # issue commands...
        for command in commands:
            p.stdin.write(command.encode('utf-8'))

        p.stdin.close()

        # Wait until process is complete
        p.communicate()

        # Serve File
        file_path = open(filepath + filename_out)
        response = HttpResponse(file_path, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename_out)
        return response

    return render(request, 'simple_upload.html')
