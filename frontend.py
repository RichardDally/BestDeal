# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import timedelta, date
import sys
import logging
import plotly
import bestdeal
import itertools


class Frontend:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.year = 2019
        self.start_date = date(year=self.year, month=1, day=1)
        self.end_date = date(year=self.year, month=12, day=31)
        self.logger.info('Display prices from [{}] to [{}]'.format(self.start_date, self.end_date))

    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def build_graph_by_product_type(self, bd, product_type, colors):
        title = html.H1(
            children='{} price history'.format(product_type),
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        )

        description = html.Div(children='Grab the best deals among all vendors easily', style={
            'textAlign': 'center',
            'color': colors['text']
        })

        no_data = True
        data = []
        for source in bd.db.get_source_identifiers():
            x = []
            y = []
            for single_date in self.daterange(self.start_date, self.end_date):
                current_date = single_date.strftime('%Y%m%d')
                minimum_record = bd.db.get_minimum_price(source['source_id'], product_type, current_date)
                if minimum_record['histo_price']:
                    x.append(single_date)
                    y.append(minimum_record['histo_price'])
            if x and y:
                no_data = False
                data.append(plotly.graph_objs.Scatter(name=source['source_name'], x=x, y=y, connectgaps=False))

        if no_data:
            self.logger.warning('No data available for model [{}] from any source'.format(product_type))
            return None

        labels = ['End of Q1', 'End of Q2', 'End of Q3', 'End of Q4']
        tickvals = [x % self.year for x in ['%s-04-01', '%s-07-01', '%s-10-01', '%s-12-31']]

        layout = plotly.graph_objs.Layout(
            title='{} Quarterly GPU prices'.format(self.year),
            xaxis=plotly.graph_objs.layout.XAxis(
                ticktext=labels,
                tickvals=tickvals
            ),
            yaxis2=dict(
                overlaying='y',
                side='right',
                showgrid=False,
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font={'color': colors['text']}
        )

        graph = dcc.Graph(
            id='{}_graph'.format(product_type),
            figure={
                'data': data,
                'layout': layout
            }
        )
        return [title, description, graph]

    def build_website(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        application = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        bd = bestdeal.BestDeal()
        children = []
        product_items = [bd.product_types, ['', 'Ti']]
        for product_type in itertools.product(*product_items):
            data = self.build_graph_by_product_type(bd, ' '.join(product_type).strip(), colors)
            if data:
                children += data

        if not children:
            raise Exception('Nothing to display...')

        application.layout = html.Div(style={'backgroundColor': colors['background']}, children=children)
        return application


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S %p')
    app = Frontend().build_website()
    app.run_server(debug=False)
