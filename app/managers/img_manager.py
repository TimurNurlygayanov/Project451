from io import BytesIO
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from os import listdir, path

from app import app, db
from imgprep import Preprocessor
from models import ImageRepresentation


def read_archive(data):
    """Read archive of images and send it to application"""
    _read_archive(data)


def _read_archive(data):
    app.logger.info("Read sample archive")
    archive = BytesIO(data)
    zip_file = ZipFile(archive, "r")
    with TemporaryDirectory() as td:
        zip_file.extractall(td)
        for file_name in listdir(td):
            _read_image(file_name, td)


def _read_image(file_name, folder_name='.', digit=None):
    app.logger.info("Read sample image: %s" % file_name)
    if digit is None:
        if '_' not in file_name:
            # Invalid file name in Archive. May be log about it?
            return

        digit, _ = file_name.split('_', 1)

        try:
            digit = int(digit)
        except ValueError:
            # Invalid file name in Archive
            return
        if digit < 0 or digit > 9:
            return

    try:
        _, extension = file_name.rsplit('.', 1)
    except ValueError:
        # File hasn't extension part!
        extension = ""
    if extension not in ['png']:
        # Unsoppurtable extension
        return

    preprocessed_image = ImageRepresentation(
        digit,
        Preprocessor.get_sample_data_fs(path.join(folder_name, file_name)))

    db.session.add(preprocessed_image)
    db.session.commit()
