import justpy as jp
from jpwidgets.widgets import HideShow


def hide_show_demo():
    """
    demonstrate the HideShow widget
    """
    wp = jp.WebPage()
    wp.debug = True
    hide_show = HideShow(
            text="Hello World",
            hide_show_label=("Hide Content","Show Content"),
            show_content=False,
            a=wp
    )
    return wp

from  jpdemo.examples.basedemo import Demo
Demo('HideShow demo',hide_show_demo)