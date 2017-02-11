from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.customxml import NetworkWriter, NetworkReader
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import imgprep
from functools import reduce


class Network():
    net = None

    def read_from_file(self, file_name):
        self.net = NetworkReader.readFromFile(file_name)

    def write_to_file(self, file_name):
        NetworkWriter.writeToFile(net, file_name)

    def init(self, hlayers=2):
        self.net = buildNetwork(imgprep.sample_pixels, hlayers, 10, bias=False)

    def train(self, dataset, epochs=None):
        trainer = BackpropTrainer(self.net, dataset.ds)
        if epochs is None:
            trainer.trainUntilConvergence()
        else:
            for e in range(epochs):
                trainer.train()

    def activate(self, blob):
        return self.net.activate(blob)


class Dataset():
    ds = None

    def __init__(self):
        self.ds = SupervisedDataSet(imgprep.sample_pixels, 10)

    def add_sample(self, blob, result):
        out = [0.] * 10
        out[result] = 1.
        self.ds.addSample(blob, out)
