from . import LatexEnvironment, begin_end


class Figure(LatexEnvironment):

    def __init__(self, caption, label, placement, context, double):
        self.caption = caption
        self.label = label
        self.context = context
        self.placement = placement
        self.double = double

    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')


    def dump(self, main_context):
        # writes everything, and caption delayed
        main_context.preamble.write(self.context.preamble.getvalue())
        env = "figure*" if self.double else "figure"

        with begin_end(main_context.f, env, self.placement) as f:
            f.write('\\captionsetup[subfloat]{farskip=0pt} % Remove the top glue from subfloats\n')
            f.write(self.context.f.getvalue())
            if self.label:
                label = '\\label{%s}' % self.label
            else:
                label = ""
            if self.caption is not None:
                f.write('\\caption{%s%s}\n' % (label, self.caption))
            else:
                f.write(label)


class StructureError(Exception):
    pass


class SubFigure(LatexEnvironment):
    def __init__(self, caption, label, context):
        self.caption = caption
        self.label = label
        self.context = context

    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')

    def subfigure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')

    def dump(self, main_context):
        body = self.context.f.getvalue()
        if self.label:
            label = "\\label{%s}" % self.label
        else:
            label = ""
        caption = self.caption
        # main_context.require_package('subfig')
        main_context.f.write('\\subfloat[%s%s]{%%\n' % (label, caption))
        main_context.f.write(body)
        main_context.f.write('}% subfloat\n')


