from StringIO import StringIO
from contracts import contract


class UsePackage:

    @contract(name='str', options='dict(str:str)')
    def __init__(self, name, options={}):
        self.name = name
        self.options = options

    def dump_preamble(self, f):
        options = dict_to_latex_option_string(self.options)
        f.write('\\usepackage[%s]{%s}\n' % (options, self.name))


def dict_to_latex_option_string(d):
    s = ""
    for k, v in d:
        if v is None:
            s += ',' + k
        else:
            s += k + '=' + v
    return s


class LatexContext:
    def __init__(self, graphics_path="."):
        self.f = StringIO()
        self.preamble = StringIO()
        self.graphics_path = graphics_path
        self.parent = None
        self.count = 0

        self.packages = {}

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

    def dump_preamble(self, f):
        for package in self.packages.values():
            package.dump_preamble(f)

    def require_package(self, name):
        if not name in self.packages:
            self.parent.use_package(name)

    def use_package(self, name, options={}):
        if self.parent is not None:
            self.parent.use_package(name, options)
        else:
            self.packages[name] = UsePackage(name, options)

