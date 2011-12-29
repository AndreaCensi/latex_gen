from ... import LatexDocument, compile_tex
import inspect
import os
import sys


class DemoStorage:
    demo_list = []
    demo_list_fail = []


def latex_gen_demo(f):
    ''' Decorator for declaring a demo. '''
    DemoStorage.demo_list.append(f)
    return f


def latex_gen_demo_failure(f):
    ''' Decorator for declaring a demo which should fail. '''
    DemoStorage.demo_list_fail.append(f)
    return f


def run_demo(demo, dirname):
    name = demo.__name__
    print('Running %s' % name)
    doc = LatexDocument()
    doc.fullpage()

    src = inspect.getsource(demo)
    doc.lstlisting(src, language='python')

    demo(doc)

    filename = os.path.join(dirname, '%s.tex' % name)
    doc.write_to_file(filename)
    compile_tex(filename)


def all_demos(argv):
    #dirname = 'latex_gen_demos/'
    dirname = '.'

    if len(argv) == 1:
        only = argv[0]
        for demo in DemoStorage.demo_list:
            if demo.__name__ == only:
                run_demo(demo, dirname)

    else:
        for demo in DemoStorage.demo_list:
            run_demo(demo, dirname)


def main():
    all_demos(sys.argv[1:])

if __name__ == '__main__':
    main()

