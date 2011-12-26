from StringIO import StringIO


class LatexContext:
    def __init__(self, graphics_path="."):
        self.f = StringIO()
        self.preamble = StringIO()
        self.graphics_path = graphics_path
        self.parent = None
        self.count = 0

    def generate_file_id(self):
        if self.parent:
            return self.parent.generate_file_id()
        f = "file%s" % self.count
        self.count += 1
        return f

    def child(self):
        ''' Generates a child context; sharing some data '''
        c = LatexContext(self.graphics_path)
        c.parent = self
        return c
