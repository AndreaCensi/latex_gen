from . import latex_gen_demo


@latex_gen_demo
def demo1(doc):
    doc.text("This is an example with a figures with two subfigures.")

    with doc.figure(caption="") as fig:
        with fig.subfigure(caption="fig1") as sub:
            sub.text("ciao")

        with fig.subfigure(caption="fig2") as sub:
            sub.text("hello")
