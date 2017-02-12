from neural import Network, Dataset
from imgprep import Preprocessor

prep = Preprocessor()
blob = prep.get_sample_data_fs('imgprep/0_test.jpg')

net = Network()
net.init()

ds = Dataset()
for i in range(10):
    ds.add_sample(blob, 0)
    ds.add_sample(blob, 2)
    ds.add_sample(blob, 4)
net.train(ds, 50)
print(net.activate(blob))
