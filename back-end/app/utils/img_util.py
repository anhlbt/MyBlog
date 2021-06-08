

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_image_filesize(filesize):
    
    if int(filesize) <= 0.5 * 1024 * 1024:
        return True
    else:
        return False


def check_resize_img():
    print("need to implement... ")