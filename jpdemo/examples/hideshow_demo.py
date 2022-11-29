import justpy as jp
from jpwidgets.widgets import HideShow


def hide_show_demo():
    """
    demonstrate the HideShow widget
    """
    wp = jp.WebPage()
    wp.debug = True
    content = jp.Div(text="Hello World")
    hide_show = HideShow(
            a=wp,
            label="Hide Content",
            content=content,
            label_if_hidden="Show Content",
            show_content=False
    )
    return wp

from  jpdemo.examples.basedemo import Demo
Demo('HideShow demo',hide_show_demo)