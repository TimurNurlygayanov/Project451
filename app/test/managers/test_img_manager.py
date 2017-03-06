from os import path, name

import pytest
import mock

from managers import img_manager


class TestImageManager(object):
    @mock.patch('app.db.session')
    @mock.patch('imgprep.Preprocessor.get_sample_data_fs')
    @mock.patch('models.ImageRepresentation.__init__')
    def test_read_image(self, model, preprocessor, session):
        model.return_value = None
        root_folder = {'nt': 'C:\\', 'posix': '\dev'}[name]
        preprocessor.return_value = 0b011

        img_manager._read_image('1_kefal.png', root_folder)
        preprocessor.assert_called_with(path.join(root_folder, '1_kefal.png'))
        model.assert_called_with(1, 0b011)
        preprocessor.reset_mock()
        model.reset_mock()

        img_manager._read_image('38_papagai.png', root_folder)
        preprocessor.assert_not_called()

        img_manager._read_image('4_diploma_work.tex', root_folder)
        preprocessor.assert_not_called()

        img_manager._read_image('rasim.png', root_folder)
        preprocessor.assert_not_called()

        img_manager._read_image('5_diploma_work.png', root_folder, digit=7)
        preprocessor.assert_called_with(
            path.join(root_folder, '5_diploma_work.png'))
        model.assert_called_with(7, 0b011)
