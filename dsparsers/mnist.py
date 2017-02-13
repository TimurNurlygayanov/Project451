import os
import numpy

from skimage import io
from dsparsers.parser import Parser
from imgprep import Preprocessor
from tqdm import tqdm
from neural import Dataset

class MNISTParser(Parser):
    "Class for downloading and parsing the famous hand-written digits dataset"

    dsurls = [
            # contains images itself
            ('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz', '.cache/mnist/images.gz', '6c95f4b05d2bf285e1bfb0e7960c31bd3b3f8a7d'),
            # contains labels (what digits are on images)
            ('http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz', '.cache/mnist/labels.gz', '2a80914081dc54586dbdf242f9805a6b8d2a15fc')
    ]

    def read_int32(self, handle):
        # inner wrapper for reading big-endian int32 from file stream
        return int.from_bytes(handle.read(4), byteorder='big')

    def parse(self, chunk_size=1024, max_samples=None):
        """Generator function for parsing samples from archives.

        Generates Dataset objects containing `chunk_size` samples each (except, perhaps, the last).
        Handles maximum of first `max_samples` (or less if there are no such) samples if specified."""

        # unzip each of both archives
        for (_, gz, _) in self.dsurls:
            os.system(str.format('gunzip -k -f {0}', gz))

        prep = Preprocessor()

        with open('.cache/mnist/images', 'rb') as fimages:
            # read magic number
            fimages.read(4)
            with open('.cache/mnist/labels', 'rb') as flabels:
                # read magic number
                flabels.read(4)

                # read number of samples and sample dimensions
                (snum, rows, cols) = [self.read_int32(fimages) for i in range(3)]

                # assert that the numbers of samples matches in both
                assert(snum == self.read_int32(flabels))

                if max_samples is not None:
                    snum = min(snum, max_samples)

                ds = Dataset()
                for i in self.progress(snum):
                    # read sample digit label
                    label = flabels.read(1)[0]

                    # read sample digit image bytes row
                    img = list(fimages.read(rows * cols))
                    # arrange bytes in a matrix and invert color
                    img = 255 - numpy.reshape(img, (rows, cols)).astype(int)

                    # preprocess and collect sample
                    blob = prep.get_sample_data_array(img)
                    ds.add_sample(blob, label)

                    # yield if either end of chunk or file
                    if (i + 1) % chunk_size == 0 or i == snum - 1:
                        yield ds
                        # don't clear yielded, but create new
                        ds = Dataset()
