import numpy

from skimage import io, filters, transform, util

# default input sample dimensions
sample_size = (64, 32)
sample_pixels = sample_size[0] * sample_size[1]


class Preprocessor(object):
    """Class for preprocessing input data into NN-suitable format."""

    @staticmethod
    def get_sample_data_array(img, file_result=None):
        """Processes grayscale array image into binary array NN-suitable sample.

        Mirrors result to file `file_result` if specified."""

        # binarize the image firstly by threshold filter
        thres = filters.threshold_otsu(img)
        img = img > thres
        # white-on-black is handled quite better, invert colors
        img = numpy.invert(img)

        # `True` bounding box corners
        lower = img.shape
        upper = (-1, -1)

        # handle each pixel
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if not img[x, y]:
                    continue
                # pixel is 'True', update the corners
                lower = tuple(map(min, lower, (x, y)))
                upper = tuple(map(max, upper, (x, y)))

        # carefully extract sample if there's at least one `True`
        if upper[0] != -1:
            img = img[lower[0]: upper[0], lower[1]: upper[1]]

        # scale image such that it fits into `sample_size` bbox
        # precisely it will fit exactly to at least one dimension
        factor = min(sample_size[i] / img.shape[i] for i in range(2))
        img = transform.rescale(img, factor).astype(bool)

        # image is scaled, but some dimension may not exactly fit
        # so we pad it
        pads = []
        for dim in range(2):
            delta = sample_size[dim] - img.shape[dim]
            before = int(delta / 2)
            after = delta - before
            # will pad almost-equal size from each side
            pads.append((before, after))

        # pad by filling new pixels with `False`
        img = numpy.pad(img, pads, 'constant', constant_values=False)

        if file_result is not None:
            # we agreed to handle black-on-white, save inverted
            io.imsave(file_result, numpy.invert(img).astype(int) * 255)

        # NNs are dealing with linear arrays, so reshape our image
        return numpy.reshape(img, (1, -1))[0].astype(int)

    def get_sample_data_fs(self, file_name, file_result=None):
        """Loads and processes image from filesystem into binary array NN-suitable sample.

        Mirrors result to file `file_result` if specified."""

        # read image in grayscale
        img = io.imread(file_name, as_grey=True)

        # just to be sure
        if img is None:
            return None

        return self.get_sample_data_array(img, file_result)
