from datetime import datetime

from jpwidgets.jpTable import Table, EchoButtonColumn, EchoTwiceButtonColumn, EchoTwiceInputDisabledButtonColumn

import justpy as jp


def show_demo():
    wp = jp.WebPage(head_html='<script src="https://cdn.tailwindcss.com"></script>', tailwind=False)
    lod=[{
                "pageTitle": "WebSci 2019",
                "acronym": "WebSci 2019",
                "ordinal": 11,
                "homepage": "http://websci19.webscience.org/",
                "title": "11th ACM Conference on Web Science",
                "eventType": "Conference",
                "startDate": datetime.fromisoformat("2019-06-30"),
                "endDate": datetime.fromisoformat("2019-07-03"),
                "inEventSeries": "WebSci",
                "country": "USA",
                "region": "US-MA",
                "city": "Boston",
                "acceptedPapers": 41,
                "submittedPapers": 120,
                "presence": "online",
                "wikicfpId": 891,
                "tibKatId":"1736060724",
                "subject": "Software engineering",
                "ISBN":"9781450370707",
                "gndId":"1221636014"
            }
    ]
    cellValidationMap = {
        'beer_servings': lambda value: value.isnumeric()
    }
    table = Table(lod=[{"index":i, **lod[0]} for i in range(5)],
                  editable=True,
                  cellValidationMap=cellValidationMap,
                  a=wp,
                  actionColumns=[
                      EchoButtonColumn(name="Echo"),
                      EchoTwiceButtonColumn(name="EchoTwice"),
                      EchoTwiceInputDisabledButtonColumn(name="EchoTwiceDisableInput")
                  ])
    return wp


if __name__ == '__main__':
    jp.justpy(show_demo, port=8400)