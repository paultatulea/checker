import timing
import sys


class CallInfo:
    """Result/Exception information of a function invocation."""

    def __init__(
        self,
        result,
        excinfo,
        start,
        stop,
        duration,
        when,
        *args
    ):
        self._result = result
        self.excinfo = excinfo
        self.start = start
        self.stop = stop
        self.duration = duration
        self.when = when

    @property
    def result(self):
        return self._result

    @classmethod
    def from_call(
        cls,
        func,
        when,
        reraise=None
    ):
    """Call func, wrapping the result in a CallInfo.
    :param func:
        The function to call. Called without arguments.
    :param when:
        The phase in which the function is called.
    :param reraise:
        Exception or exceptions that shall propogate if raised
        by the function, instead of being wrapped in the CallInfo.
    """
    excinfo = None
    start = timing.time()
    try:
        result = func()
    except BaseException:
        # pytest uses a custom class for ExceptionInfo
        # keep it simple and use sys.exc_info()
        excinfo = sys.exc_info()
        # Tuple[Type['_E'], '_E', TracebackType],
        # type -> type of exception being handled
        # value -> instance of exception type
        # tb -> traceback object
        if reraise is not None and isinstance(excinfo[1], reraise):
            raise
        result = None
    stop = timing.time()
    duration = stop - start
    return cls(
        start=start,
        stop=stop,
        duration=duration,
        when=when,
        result=result,
        excinfo=excinfo
    )
