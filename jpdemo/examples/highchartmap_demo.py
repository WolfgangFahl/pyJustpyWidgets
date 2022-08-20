'''
Created on 2022-08-22

@author: wf
'''
import justpy as jp

my_chart_def = """
{
 chart: {
    map: 'custom/europe',
    borderWidth: 1
  },

  title: {
    text: 'Nordic countries'
  },

  subtitle: {
    text: 'Demo of drawing all areas in the map, only highlighting partial data'
  },

  legend: {
    enabled: false
  },

  series: [{
    name: 'Country',
    data: [
      ['is', 1],
      ['no', 1],
      ['se', 1],
      ['dk', 1],
      ['fi', 1]
    ],
    dataLabels: {
            enabled: true,
            color: '#FFFFFF'
        },
    }]
}
"""

def chart_test():
    wp = jp.WebPage()
    #<script src="https://code.highcharts.com/maps/highmaps.js"></script>
    wp.head_html = """
    <script src="https://code.highcharts.com/maps/9.2.2/highmaps.js"></script>
    <script src="https://code.highcharts.com/mapdata/custom/europe.js"></script>
    """
    my_chart = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2 h-screen', options=my_chart_def)
    my_chart.options.chart.type = 'map'
    my_chart.options.series[0].name = 'Test chart'
    my_chart.options.title.text = 'Data'
    return wp

from  jpdemo.examples.basedemo import Demo
Demo('highchart maps demo',chart_test)
