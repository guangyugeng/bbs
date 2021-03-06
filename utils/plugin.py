from flask_wtf.csrf import CsrfProtect
from flask_uploads import (
    configure_uploads,
    UploadSet,
    patch_request_class,
    IMAGES
)

csrf = CsrfProtect()

uploaded_avatars = UploadSet('AVATAR', IMAGES)