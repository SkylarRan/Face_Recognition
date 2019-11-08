import uuid
import os
from err import FormatError

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_blacklist_image(file):
    if not (file and allowed_file(file.filename)):
        raise FormatError("Image format error!")

    folder = os.path.join(os.getcwd(), "static", "blacklist")
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = str(uuid.uuid1()) + ".jpg"
    fullname = os.path.join(folder, filename)
    file.save(fullname)
    return "blacklist/" + filename

