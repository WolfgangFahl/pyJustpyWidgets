'''
@author Tim Holzheim
2022-06
'''
from datetime import datetime

from jpwidgets.jpTable import Table, EchoButtonColumn, EchoTwiceButtonColumn, EchoTwiceInputDisabledButtonColumn

import justpy as jp
import argparse
import socket

class TableDemo:
    '''
    demonstration for jpTable widget
    '''
    def show_demo(self):
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
        self.table = Table(lod=[{"index":i, **lod[0]} for i in range(5)],
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
    parser = argparse.ArgumentParser(description='jpTable Demo')
    parser.add_argument('--host',default=socket.getfqdn())
    parser.add_argument('--port',type=int,default=8000)
    args = parser.parse_args()
    tableDemo=TableDemo()
    jp.justpy(tableDemo.show_demo, host=args.host,port=args.port)