import numpy

from app.dsparsers.mnist import MNISTParser
from app.neural import Dataset, Network
from app.imgprep import Preprocessor

parser = MNISTParser()
parser.load_urls()

net = Network()
net.init(32)

for ds in parser.parse(max_samples=256):
    net.train(ds, 50, progress=True)

prep = Preprocessor()
blob = prep.get_sample_data_fs('imgprep/0_test.jpg')
print(numpy.round(net.activate(blob), 3))
