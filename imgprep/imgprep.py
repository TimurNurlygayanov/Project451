from skimage import io, filters, transform, util
import numpy

sample_size = (64, 32) # default input sample dimensions
sample_pixels = sample_size[0] * sample_size[1]

class Preprocessor():
    """ Class for preprocessing input data
    into NN-suitable format
    """

    def get_sample_data_fs(self, file_name, file_result = None):
        """ Method sampling image loaded from filesystem
        into a blob tuple
        """

        img = io.imread(file_name, as_grey=True)
        if img is None:
            return None

        # TODO the following is working sufficiently only with black-on-white images
        thres = filters.threshold_otsu(img)
        img = img > thres
        img = numpy.invert(img) # white-on-black is handled quite better

        lower = img.shape
        upper = (-1, -1)

        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if not img[x, y]:
                    continue
                lower = tuple(map(min, lower, (x, y)))
                upper = tuple(map(max, upper, (x, y)))

        if upper[0] != -1:
            img = img[lower[0] : upper[0], lower[1] : upper[1]]

        factor = min(sample_size[i] / img.shape[i] for i in range(2))
        img = transform.rescale(img, factor).astype(bool)

        pads = []
        for dim in range(2):
            delta = sample_size[dim] - img.shape[dim]
            before = int(delta / 2)
            after = delta - before
            pads.append((before, after))

        img = numpy.pad(img, pads, 'constant', constant_values=False)

        if file_result is not None:
            io.imsave(file_result, img.astype(int) * 255)

        return numpy.reshape(img, (1, -1))[0].astype(int)
