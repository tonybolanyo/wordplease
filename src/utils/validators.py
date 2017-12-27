# https://docs.djangoproject.com/en/2.0/ref/validators/
# List of MIME types: https://www.sitepoint.com/mime-types-complete-list/

from django.core.exceptions import ValidationError


class ContentTypeValidator:

    """
    Valida que el `content_type` de un archivo esté contenido el la lista
    `accepted_types`.
    """

    message = 'Content type not accepted'
    code = 'content_type'

    def __init__(self, accepted_types):
        self.accepted_types = accepted_types

    def __call__(self, file):
        content_type = file.file.content_type
        if content_type not in self.accepted_types:
            raise ValidationError(message=self.message, code=self.code)


class MaxFileSizeValidator:

    """
    Valida que un archivo sea menor que el tamaño máximo permitido.
    El tamaño se especifica en bytes.
    """

    message = 'File is too large'
    code = 'max_file_size'

    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if self.max_size < file.size:
            raise ValidationError(message=self.message, code=self.code)
