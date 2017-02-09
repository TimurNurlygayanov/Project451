import subprocess
import uuid
import numpy
from PIL import Image, ImageDraw, ImageOps


class Converter():
    """ This class allows convert image files to the binary array,
        which can be loaded to ai_core.
    """

    factor = 125 # factor to make negative copy of initial image

    size = (100, 200)  # we will modify all images to the same
                       # size to make sure we will have the same size of
                       # input data for ai_core input.

    def get_normalized_image(self, file_name, save_as_file=None):
        """ This method converts any image file to the binary array. """

        cmd = "convert {0} -monochrome -normalize {1}"
        new_file_name = "{0}.jpg".format(uuid.uuid4().hex)
        proc = subprocess.Popen(cmd.format(file_name, new_file_name),
                                shell=True)
        proc.communicate()

        image = Image.open(new_file_name)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        start_pixel = (height, width)
        end_pixel = (0, 0)

        print "result size: ", (height, width)

        # get binnary array for image:
        result = numpy.zeros((height, width))
        for i in xrange(height):
            for j in xrange(width):
                value = [pix[j, i][k] for k in xrange(3)]
                if (sum(value) < self.factor):
                    result[i][j] = 0

                    # find the boundaries of the image
                    # to ignore a white space:
                    if start_pixel[0] > i:
                        start_pixel = (i, start_pixel[1])
                    if start_pixel[1] > j:
                        start_pixel = (start_pixel[0], j)
                    if end_pixel[0] < i:
                        end_pixel = (i, end_pixel[1])
                    if end_pixel[1] < j:
                        end_pixel = (end_pixel[0], j)
                else:
                    result[i][j] = 1

        # determine the size of area with the image:
        height = end_pixel[1] - start_pixel[1]
        width = end_pixel[0] - start_pixel[0]

        # resize original image
        image = image.resize((height, width), Image.ANTIALIAS)
        draw = ImageDraw.Draw(image)

        # generate new image with only important data:
        for i in xrange(height):
            for j in xrange(width):
                k = result[j + start_pixel[0]][i + start_pixel[1]]
                draw.point((i, j), (int(255*k), int(255*k), int(255*k)))

        # resize the image to the default size (all images should have
        # the same size to use it for ai_core component
        image = image.resize(self.size, Image.ANTIALIAS)
        pix = image.load()

        # generate binary array with the right size for ai_core:
        data = numpy.zeros((height, width))
        for i in xrange(height):
            for j in xrange(width):
                value = [pix[j, i][k] for k in xrange(3)]
                if (sum(value) > self.factor):
                    data[i][j] = 1

        if save_as_file is not None:
            image.save(save_as_file, "JPEG")

        del draw
        del image

        return data


# TODO: delete it and write unit tests:
t = Converter()
t.get_normalized_image("0_test.jpg")
