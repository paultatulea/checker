"""Implementation of pytest-inspired marks.
See src/_pytest/mark/structures.py for pytest implementation.
"""
import inspect


class Mark:
    def __init__(
        self,
        name,
        args,
        kwargs
    ):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def combined_with(self, other):
        assert self.name == other.name
        return Mark(
            self.name,
            self.args + other.args,
            dict(self.kwargs, **other.kwargs)
        )


class MarkDecorator:
    """When a ``MarkDecorator`` is called, it does the following:
    1. If called with a single class as its only positional argument and no
       additional keyword arguments, it attaches the mark to the class so it
       gets applied automatically to all test cases found in that class.

    2. If called with a single function as its only positional argument and
       no additional keyword arguments, it attaches the mark to the function,
       containing all the arguments already stored internally in the
       ``MarkDecorator``.

    3. When called in any other case, it returns a new ``MarkDecorator``
       instance with the original ``MarkDecorator``'s content updated with
       the arguments passed to this call.

    Note: The rules above prevent a ``MarkDecorator`` from storing only a
    single function or class reference as its positional argument with no
    additional keyword or positional arguments. You can work around this by
    using `with_args()`.
    """

    def __init__(self, mark):
        self.mark = mark

    @property
    def name(self):
        """Alias for mark.name."""
        return self.mark.name

    @property
    def args(self):
        """Alias for mark.args."""
        return self.mark.args

    @property
    def kwargs(self):
        """Alias for mark.kwargs."""

    def __repr__(self):
        return f'<MarkDecorator {repr(self.mark)}'

    def with_args(self, *args, **kwargs):
        """Return a MarkDecorator with extra arguments added."""
        mark = Mark(self.name, args, kwargs)
        return MarkDecorator(self.mark.combined_with(mark))

    def __call__(self, *args, **kwargs):
        """Call MarkDecorator."""
        if args and not kwargs:
            func = args[0]
            is_class = inspect.isclass(func)
            if len(args) == 1 and (hasattr(func, '__call__') or is_class):
                store_mark(func, self.mark)
                return func
        return self.with_args(*args, **kwargs)


def normalise_mark_list(mark_list):
    """Normalise the marker decorating helpers."""
    # Get the Mark object from each MarkDecorator
    extracted = [getattr(mark, 'mark', mark) for mark in mark_list]
    # Ensure each mark is the correct class instnace
    for mark in extracted:
        if not isinstance(mark, Mark):
            raise TypeError(f'Got {repr(mark)} instead of Mark')
    return [x for x in extracted if isinstance(x, Mark)]


def get_unpacked_marks(obj):
    """Get the unpacked marks that are stored on an object"""
    mark_list = getattr(obj, 'icmark', [])
    if not isinstance(mark_list, list):
        mark_list = [mark_list]
    return normalise_mark_list(mark_list)


def store_mark(obj, mark):
    """Store mark on an object."""
    assert isinstance(mark, Mark)
    obj.icmark = get_unpacked_marks(obj) + [mark]


class MarkFactory:
    def __init__(self):
        self._markers = set()

    def __getattr__(self, name):
        """Generate a new MarkDecorator with the given name"""
        # Do not allow marker to start with

        if name[0] == '_':
            raise AttributeError('Marker must NOT start with underscore')
        return MarkDecorator(Mark(name, (), {}))


mark_factory = MarkFactory()


skip = mark_factory.skip


@ mark_factory.skip
@ mark_factory.sanity
def check_add():
    result = 5
    expected = 10
    assert result == expected


check_add()
