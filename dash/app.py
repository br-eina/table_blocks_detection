# -*- coding: utf-8 -*-
import sys
sys.path.append(".")
from os.path import exists
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
from inv_processing import (
    detect_lines_symbols,
    constr_rows,
    constr_blocks,
    detect_table,
    predict_label,
    recognize_tesser
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a document image')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                # 'position': 'fixed'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),

        # Hidden div
        html.Div(id='hidden-div', style={'display': 'none'}),

        html.Button('Initiate processing', id='btn-processing', n_clicks=0),

        html.Div(id='scripts-status', children=[
            html.Div(
            id='symbols-detected'
            ),

            html.Div(
                id='rows-constructed'
            ),

            html.Div(
                id='textblocks-constructed'
            ),

            html.Div(
                id='tables-detected'
            ),

            html.Div(
                id='lables-predicted'
            ),

            html.Div(
                id='data-recognized'
            ),

            html.Div(
                id='recognized-info',
                style={'textAlign': 'center'}
            )
        ])
    ],
    style={'width': '33%', 'display': 'inline-block', 'height': '600px'}
    ),

    # html.Div(
    #     className='vertical-line',
    #     style={
    #         'width': '10px',
    #         'height': '100%',
    #         'background-color': 'black',
    #         'display': 'inline-block'
    #     }
    # ),

    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Visualization', children=[
                html.Div([
                    html.Div(
                        id='selected-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        id='blocks-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    )
                ])
            ]),
            dcc.Tab(label='Debug', children=[
                html.Div([
                    html.Div(
                        id='symbols-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        id='rows-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    )
                ]),
                html.Div([
                    html.Div(
                        id='textblocks-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        id='tables-image',
                        style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}
                    )
                ])
            ])
        ])
    ],
    style={'width': '65%', 'display': 'inline-block', 'padding': '15px', 'position': 'absolute', 'top': '0'}
    )
])

def parse_image(contents, filename):
    return html.Div([
        html.H4(f'{filename}', style={'textAlign': 'center'}),
        html.Img(
            src=contents,
            # style={'height': '750px', 'width': '500px'}
            style={'height': '100%', 'width': '100%'}
        )
    ]
    )

# Displaying the input image
@app.callback(Output('selected-image', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename')])
def show_selected_image(contents, filename):
    if contents is not None:
        children = parse_image(contents, 'Input image:')
        return children


# Clear scripts status
@app.callback([Output('scripts-status', 'children'),
               Output('hidden-div', 'children')],
              [Input('btn-processing', 'n_clicks')])
def clear_scripts_status(n_clicks):
    if n_clicks > 0:
        return ([
            html.Div(
            id='symbols-detected'
            ),

            html.Div(
                id='rows-constructed'
            ),

            html.Div(
                id='textblocks-constructed'
            ),

            html.Div(
                id='tables-detected'
            ),

            html.Div(
                id='lables-predicted'
            ),

            html.Div(
                id='data-recognized'
            ),

            html.Div(
                id='recognized-info',
                style={'textAlign': 'center'}
            )
        # ])
        ], 'scripts_cleared')
    return (None, None)

# Symbols are detected
@app.callback([Output('symbols-detected', 'children'),
               Output('symbols-image', 'children')],
              [Input('hidden-div', 'children')],
            #   [Input('btn-processing', 'n_clicks')],
              [State('upload-image', 'filename')])
def detect_symbols(children, filename):
    if children:
        image_name = filename[:8]
        image_path = f'docs/{filename}'
        detect_lines_symbols.main(image_name, image_path)

        image_path = f'results/{image_name}/{image_name}_text.jpg'
        encoded_image = base64.b64encode(open(image_path, 'rb').read())
        contents = 'data:image/png;base64,{}'.format(encoded_image.decode())
        children = parse_image(contents, 'Symbols:')

        return (html.Div('Symbols detection ... Done.'), children)
    return (None, None)

# Rows are constructed
@app.callback([Output('rows-constructed', 'children'),
               Output('rows-image', 'children')],
              [Input('symbols-detected', 'children')],
              [State('upload-image', 'filename')])
def contsruct_rows(children, filename):
    if children:
        image_name = filename[:8]
        image_path = f'docs/{filename}'
        constr_rows.main(image_name, image_path)

        image_path = f'results/{image_name}/{image_name}_char_rows.jpg'
        encoded_image = base64.b64encode(open(image_path, 'rb').read())
        contents = 'data:image/png;base64,{}'.format(encoded_image.decode())
        children = parse_image(contents, 'Rows:')

        return (html.Div('Symbols rows construction ... Done.'), children)
    return (None, None)

# Textblocks are constructed
@app.callback([Output('textblocks-constructed', 'children'),
               Output('textblocks-image', 'children')],
              [Input('rows-constructed', 'children')],
              [State('upload-image', 'filename')])
def contsruct_textblocks(children, filename):
    if children:
        image_name = filename[:8]
        image_path = f'docs/{filename}'
        constr_blocks.main(image_name, image_path)

        image_path = f'results/{image_name}/{image_name}_blocks.jpg'
        encoded_image = base64.b64encode(open(image_path, 'rb').read())
        contents = 'data:image/png;base64,{}'.format(encoded_image.decode())
        children = parse_image(contents, 'Textblocks:')

        return (html.Div('Textblocks construction ... Done.'), children)
    return (None, None)

# Tables are detected
@app.callback([Output('tables-detected', 'children'),
               Output('tables-image', 'children')],
              [Input('textblocks-constructed', 'children')],
              [State('upload-image', 'filename')])
def table_detection(children, filename):
    if children:
        image_name = filename[:8]
        image_path = f'docs/{filename}'
        detect_table.main(image_name, image_path)

        image_path = f'results/{image_name}/{image_name}_tables.jpg'
        encoded_image = base64.b64encode(open(image_path, 'rb').read())
        contents = 'data:image/png;base64,{}'.format(encoded_image.decode())
        children = parse_image(contents, 'Tables:')

        return (html.Div('Tables detection ... Done.'), children)
    return (None, None)

# Labels are predicted
@app.callback(Output('lables-predicted', 'children'),
              [Input('tables-detected', 'children')],
            #   [Input('btn-processing', 'n_clicks')],
              [State('upload-image', 'filename')])
def labels_prediction(children, filename):
    if children:
        image_name = filename[:8]
        predict_label.main(image_name)
        return html.Div('Labels prediction ... Done.')

# Displaying labeled image
@app.callback(Output('blocks-image', 'children'),
              [Input('lables-predicted', 'children')],
              [State('upload-image', 'filename')])
def show_blocks_image(children, filename):
    if children:
        image_path = f'predictions/{filename[:8]}_pred.jpg'
        encoded_image = base64.b64encode(open(image_path, 'rb').read())
        contents = 'data:image/png;base64,{}'.format(encoded_image.decode())
        children = parse_image(contents, 'Processed image:')
        return children

# Data is recognized:
@app.callback(Output('data-recognized', 'children'),
              [Input('lables-predicted', 'children')],
            #   [Input('btn-processing', 'n_clicks')],
              [State('upload-image', 'filename')])
def data_recognition(children, filename):
    if children:
        image_name = filename[:8]
        recognize_tesser.main(image_name)
        return html.Div('Data recognition ... Done.')

# Displaying recognized info
@app.callback(Output('recognized-info', 'children'),
              [Input('data-recognized', 'children')],
              [State('upload-image', 'filename')])
def show_recognized_info(children, filename):
    if children:
        image_name = filename[:8]
        folder_txt = f'tesser_data/{image_name}/recognized'

        doc_id = ''
        if exists(f'{folder_txt}/full_doc_id.txt'):
            with open(f'{folder_txt}/full_doc_id.txt', encoding='utf-8') as f:
                for line in f:
                    doc_id += line

        info = ''
        if exists(f'{folder_txt}/full_info.txt'):
            with open(f'{folder_txt}/full_info.txt', encoding='utf-8') as f:
                for line in f:
                    info += line

        total = ''
        if exists(f'{folder_txt}/full_total.txt'):
            with open(f'{folder_txt}/full_total.txt', encoding='utf-8') as f:
                for line in f:
                    total += line

        verif = ''
        if exists(f'{folder_txt}/full_verif.txt'):
            with open(f'{folder_txt}/full_verif.txt', encoding='utf-8') as f:
                for line in f:
                    verif += line

        return html.Div([
            html.H3(
                children='Recognized information:'
                # style={'textAlign': 'center'}
            ),

            html.Div([
                html.H5('Название документа ("doc_id"): ',
                         style={'textAlign': 'center'}),
                dcc.Textarea(
                    id='doc_id',
                    value=doc_id,
                    style={'textAlign': 'center', 'width': '100%', 'height': '100%'}
                )
            ]
            # style={'display': 'inline-block'}
            ),

            html.Div([
                html.H5('Информация об участниках сделки ("info"): ',
                         style={'textAlign': 'center'}),
                dcc.Textarea(
                    id='info',
                    value=info,
                    style={'textAlign': 'center', 'width': '100%', 'height': '250px'}
                )
            ]
            # style={'display': 'inline-block'}
            ),

            html.Div([
                html.H5('Итого ("total"): ',
                         style={'textAlign': 'center'}),
                dcc.Textarea(
                    id='total',
                    value=total,
                    style={'textAlign': 'center', 'width': '100%', 'height': '130px'}
                )
            ]
            # style={'display': 'inline-block'}
            ),

            html.Div([
                html.H5('Верификация ("verif"): ',
                         style={'textAlign': 'center'}),
                dcc.Textarea(
                    id='verif',
                    value=verif,
                    style={'textAlign': 'center', 'width': '100%', 'height': '100px'}
                )
            ]
            # style={'display': 'inline-block'}
            )
        ])



if __name__ == '__main__':
    app.run_server(debug=True)