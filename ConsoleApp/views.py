import os
import random
import shutil
import string
import subprocess
from ConsoleAppIntegration.settings import STATIC_ROOT, MEDIA_ROOT

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.datetime_safe import datetime
from django.utils.encoding import smart_str


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfiles']:
        myfiles = request.FILES.getlist('myfiles')
        upload_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
        directory = datetime.now().strftime('\\%Y%m%d\\') + upload_id + '\\'

        if len(myfiles) > 1:
            for file in myfiles:
                fs = FileSystemStorage(location=MEDIA_ROOT + directory)
                fs.save(file.name, file)

        else:
            file = myfiles[0]
            fs = FileSystemStorage(location=MEDIA_ROOT + directory)
            fs.save(file.name, file)

        uploaded_file_path = MEDIA_ROOT + directory
        filepath = MEDIA_ROOT + directory
        filename_out = "result_" + os.path.splitext(upload_id)[0] + ".doc"

        app = STATIC_ROOT + "\\ConsoleApplication.exe"
        p = subprocess.Popen([str(app)], stdin=subprocess.PIPE)

        # Commands to send
        # TODO: scan entire directory regardless since a single file will be the only one in the dir
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

        # delete files older than today
        for f in os.scandir(MEDIA_ROOT):
            folder = os.fsdecode(f)
            current_folder = MEDIA_ROOT + datetime.now().strftime('\\%Y%m%d')
            if folder != current_folder:
                shutil.rmtree(f)

        # Serve File
        file_path = open(filepath + filename_out)
        response = HttpResponse(file_path, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename_out)
        return response

    return render(request, 'simple_upload.html')
