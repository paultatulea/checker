from nodes import FileCollector


class Session(FileCollector):
    def __init__(self, config):
        super().__init__(
            config.rootdir,
            parent=None,
            config=config,
            session=self,
            nodeid=''
        )
        self.testsFailed = 0
        self.testsCollected = 0
        self.shouldStop = False
        self.shouldFail = False
        self.startDir = config.invocation_dir

    @classmethod
    def from_config(cls, config):
        session = cls._create(config)
        return session

    def runtest_logreport(self, report):
        if report.failed:
            self.testsFailed += 1

    collectreport = runtest_logreport

    def perform_collect(self, args=None):
        """Perform collection phase for this session.

        Recursively expands collecters collected from the session to their items,
        and only items are returned.
        """
        if args is None:
            args = self.config.args

        _notfound = []
        _initial_parts = []
        items = []
        try:
            initialpaths = []

    def collect(self):
        ...
