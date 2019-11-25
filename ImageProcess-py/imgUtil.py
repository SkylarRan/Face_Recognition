import uuid
import os
from err import FormatError

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_blacklist_image(file, id):
    if not (file and allowed_file(file.filename)):
        raise FormatError("Image format error!")

    folder = os.path.join(os.getcwd(), "static", "blacklist")
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = id + ".jpg"
    fullname = os.path.join(folder, filename)
    file.save(fullname)
    return "blacklist/" + filename

def remove_image(category, id):
    filename = "static/" + category + "/" + id + ".jpg"
    if os.path.exists(filename):
        os.remove(filename)

