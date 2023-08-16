from django import template
import os
import math
register = template.Library()
#@register.filter(name="ext")
@register.filter()

def ext(value,func):
    hund_twen = 128849018880
    media_dir = r"F:\DATE\server_media\cloud_media/"
    try :
        if func == str(1):
            path = str(media_dir) + str(value)
            total = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)
            export = '{:.2%}'.format(int(total) / int(hund_twen)) #120GB,128849018880
        elif func == str(2):
            path = str(media_dir) + str(value)
            total = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)
            units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
            i = math.floor(math.log(total, 1024)) if total > 0 else 0
            total = round(total / 1024 ** i, 2)
            export = f"{total} {units[i]}"
        elif func == str(3):
            path = str(media_dir) + str(value)
            total = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)
            total = int(hund_twen) - total
            if total >= 10737418240 :
                export = 'bg-info'
            else :
                export = 'bg-danger'
        elif func == str(4):
            try :
                path = str(media_dir) + str(value)
                total = 0
                with os.scandir(path) as it:
                    for entry in it:
                        if entry.is_file():
                            total += entry.stat().st_size
                        elif entry.is_dir():
                            total += get_dir_size(entry.path)

                if total >= int(hund_twen) :
                    export = 'disabled'
                else:
                    export = 'active'
            except :
                export = 'active'
        elif func == str(5):
            path = str(media_dir) + str(value)
            total = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)

            if total >= int(hund_twen) :
                export = ''
            else:
                export = 'hidden'
        else:
            path = str(media_dir) + str(value) + '/' + str(func)
            total = os.path.getsize(path)
            units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
            i = math.floor(math.log(total, 1024)) if total > 0 else 0
            total = round(total / 1024 ** i, 2)
            export = f"{total} {units[i]}"
    except:
        export = 'hidden'
    return str(export)
