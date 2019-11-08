class FormatError(Exception):
    def __init__(self, errMsg):
        super().__init__(self)
        self.errMsg = errMsg

    def __str__(self):
        return self.errMsg