"""Implementation of nodes."""
import os

SEP = '/'


class NodeMeta(type):

    def _create(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class Node(metaclass=NodeMeta):
    """Base class for Collector and Item, components
    of test collection tree.
    Collector subclasses have children; Items are leaf nodes.
    """

    def __init__(
        self,
        name,
        parent=None,
        config=None,
        session=None,
        path=None,
        nodeid=None
    ):
        self.name = name  # Unique name within scope of parent node
        self.parent = parent  # The parent collector node

        # TODO config object

        # TODO session object

        # TODO NodeKeywords
        self.keywords = None

        self.own_markers = []

        if nodeid is not None:
            self._nodeid = nodeid
        else:
            if not self.parent:
                raise TypeError('nodeid or parent must be provided')
            self._nodeid = self.parent.nodeid
            if self.name != '()':
                self._nodeid += '::' + self.name

    @classmethod
    def from_parent(cls, parent, **kwargs):
        """Constructor for Nodes."""
        if 'config' in kwargs:
            raise TypeError('config is not a valid argument for from_parent')
        if 'session' in kwargs:
            raise TypeError('session is not a valid argument for from_parent')
        return cls._create(parent, **kw)


class Collector(Node):
    """Collector instances create children through collect()
    and iteratively build a tree.
    """

    def collect(self):
        """Return list of children (items and collectors) for this node."""
        raise NotImplementedError('Abstract')


class FileCollector(Collector):
    def __init__(
        self,
        path,
        parent=None,
        config=None,
        session=None,
        nodeid=None
    ):
        name = os.path.basename(path)
        if parent is not None:
            rel = os.path.relpath(path, parent.path)
            name = rel
            name = name.replace(os.sep, SEP)
        self.path = path
        session = session or parent.session
        if nodeid is None:
            nodeid = os.path.relpath(path, session.config.rootdir)
            nodeid = nodeid.replace(os.sep, SEP)

        super().__init__(name, parent, config, session, nodeid=nodeid)

    @classmethod
    def from_parent(cls, parent, *, path, **kwargs):
        """Public constructor.
        These arguments are only allowed in Python 3.X.
        Specifies path as a keyword-only argument.
        """
        return super().from_parent(parent=parent, path=path, **kwargs)


class Item(Node):
    """Basic test invocation item."""

    def __init__(
        self,
        name,
        parent=None,
        config=None,
        session=None,
        nodeid=None
    ):
        super().__init__(name, parent, config, session, nodeid=nodeid, path=path)

    def runtest(self):
        raise NotImplementedError('Abstract')
