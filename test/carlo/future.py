class Future:
    _ready = False
    _pass = False
    _data = None

    def __init__(self, func):
        # todo: thread off this call
        func(self._success, self._failure)

    def _success(self, *args):
        _pass = True
        _data = args
        _ready = True

    def _failure(self, *args):
        _pass = False
        _data = args
        _ready = True

    def then(self, success, failure):
        self.success(success)
        self.failure(failure)
        return Future(...)

    def success(self, func):
        pass

    def failure(self, func):
        pass

    @property
    def ready(self):
        return _ready

    @classmethod
    def wait(cls, futures):
        pass

    @classmethod
    def race(cls, futures):
        pass
