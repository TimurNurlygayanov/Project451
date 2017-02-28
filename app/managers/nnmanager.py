from functools import wraps
from neural import Network

def _do_decorator(net_func, for_all=True):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, net_names=[], **kwargs):
            def net_func_call(net):
                return net_func(net, *args, **kwargs)

            if for_all:
                result = self.do_for_all(net_func_call)
            else:
                result = self.do_for_some(net_func_call, net_names)

            return result
        return wrapper
    return decorator

def _net_train(net, *args, **kwargs):
    return net.train(*args, **kwargs)

def _net_activate(net, *args, **kwargs):
    return net.activate(*args, **kwargs)

class NNManager(object):

    nets = {}

    def add(self, name, net):
        if name in self.nets:
            return False
        self.nets[name] = net

    def add_new(self, name, *args, **kwargs):
        net = Network()
        net.init(*args, **kwargs)
        return self.add(name, net)

    def get(self, name):
        if name not in self.nets:
            return None
        return self.nets[name]

    def do_for_all(self, func):
        return self.do_for_some(func, self.nets.keys())

    def do_for_some(self, func, net_names=[]):
        result = {}
        for name in net_names:
            if name not in self.nets:
                # TODO should we inform about it?
                continue
            result[name] = func(self.nets[name])
        return result

    @_do_decorator(_net_train)
    def train_all(self, *args, **kwargs):
        pass

    @_do_decorator(_net_train, False)
    def train_some(self, *args, net_names=[], **kwargs):
        pass

    @_do_decorator(_net_activate)
    def activate_all(self, *args, **kwargs):
        pass

    @_do_decorator(_net_activate, False)
    def activate_some(self, *args, net_names=[], **kwargs):
        pass
