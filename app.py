from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from flask import Flask
import numpy as np
from PIL import Image
import io
import base64
import requests

END_POINT = "https://neural-style-transfer-zekrs5pysa-uc.a.run.app/"

# UPLOAD BUTTON
upload_icon = DashIconify(icon="hugeicons:image-upload", style={"marginLeft": 5})
img_upload_button = dbc.Button(id='img-upload-btn', children=['Upload image', upload_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')
sty_upload_button = dbc.Button(id='sty-upload-btn', children=['Upload style', upload_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')
fi_upload_button = dbc.Button(id='fi-upload-btn', children=['Upload first image', upload_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')
si_upload_button = dbc.Button(id='si-upload-btn', children=['Upload second image', upload_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')

# STYLIZE BUTTON
stylize_icon = DashIconify(icon="raphael:magic", style={"marginLeft": 5})
stylize_button = dbc.Button(id='stylize-btn', children=['Stylize', stylize_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')

# SCAN BUTTON
scan_icon = DashIconify(icon="tabler:photo-scan", style={"marginLeft": 5})
scan_button = dbc.Button(id='scan-btn', children=['Scan', scan_icon], style={'marginBottom': '20px', 'background-color': '#000080'}, size='lg')

# LAYOUT
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY], suppress_callback_exceptions=True)
server = app.server
app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(tab_id = 'tab1', label="Fusion Canvas", tabClassName='flex-grow-1 text-center', label_style={'color': '#000080'}, active_label_style={'color': '#FFFFFF', 'background-color': '#000080'}),
        dbc.Tab(tab_id = 'tab2', label="Art Sync", tabClassName='flex-grow-1 text-center', label_style={'color': '#000080'}, active_label_style={'color': '#FFFFFF', 'background-color': '#000080'}),
    ], id="tabs", active_tab='tab1', style={'fontFamily': 'Apple-chancery, cursive', 'fontWeight': 'bold', 'fontSize': '28px'}),
    html.Div(id='tabs-content')
])

# TABS CALLBACK
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'active_tab')
)
def render_content(tab):
    if tab == 'tab1':
        return dbc.Container([
            dbc.Container([
                html.H2("Welcome to the mixing magic!", style={'marginTop': '10px', 'textAlign': 'center'}),
                html.H4("Upload your art and the style you want it to be in, and stylize your art."),
                html.P(html.I("*Please note that the files should be in .jpg format. educational purpose, refrain from using copyright images"), style={'textAlign': 'right'}),
                html.Div([
                    html.Div([
                        dcc.Upload(
                            id='upload-image',
                            children=img_upload_button,
                            multiple=False
                        ),
                        dcc.Loading(
                            id='loading-output-image',
                            children=html.Div(id='output-image'),
                            type='default'
                        ),
                        dcc.Upload(
                            id='upload-style',
                            children=sty_upload_button,
                            multiple=False,
                            style={'marginTop': '50px'}
                        ),
                        dcc.Loading(
                            id='loading-output-style',
                            children=html.Div(id='output-style'),
                            type='default'
                        )
                    ], style={'display': 'inline-block', 'width': '750px'}),
                    html.Div([
                        stylize_button,
                        dcc.Loading(
                            html.Img(id='stylized-image', style={'maxWidth': '450px', 'maxHeight': '450px'})
                        )
                    ], style={'display': 'inline-block', 'verticalAlign': 'top'})
                ], style={'marginBottom': '50px'}),
                html.Hr()
            ]),
            dbc.Container([
                html.Footer([
                    html.H6("This app is built on the foundational principles of neural style transfer developed by Mr. Shafik Quoraishee, with frontend design by Ms. Manali Jain."),
                    html.H6(["If you wish to join or support the ARTISTvsAI campaign, drop a mail at ",
                        html.A("jmanali1996@gmail.com", href='mailto:jmanali1996@gmail.com', target='_blank')])
                ])
            ])
        ], style={'color': '#000080'})
    else:
        return dbc.Container([
            dbc.Container([
                html.H2("Let's evaluate the creativity!", style={'marginTop': '10px', 'textAlign': 'center'}),
                html.H4("Upload the two art images and scan the similarity percentage."),
                html.P(html.I("*Please note that the files should be in .jpg format and of the same size."), style={'textAlign': 'right'}),
                html.Div([
                    html.Div([
                        dcc.Upload(
                            id='upload-first-image',
                            children=fi_upload_button,
                            multiple=False
                        ),
                        dcc.Loading(
                            id='loading-output-first-image',
                            children=html.Div(id='output-first-image'),
                            type='default'
                        ),
                        dcc.Upload(
                            id='upload-second-image',
                            children=si_upload_button,
                            multiple=False,
                            style={'marginTop': '50px'}
                        ),
                        dcc.Loading(
                            id='loading-output-second-image',
                            children=html.Div(id='output-second-image'),
                            type='default'
                        )
                    ], style={'display': 'inline-block', 'width': '750px'}),
                    html.Div([
                        scan_button,
                        dcc.Loading(
                            html.Img(id='scaned-image', style={'maxWidth': '450px', 'maxHeight': '450px'})
                        )
                    ], style={'display': 'inline', 'verticalAlign': 'top'})
                ], style={'marginBottom': '50px'}),
                html.Hr()
            ]),
            dbc.Container([
                html.Footer([
                    html.H6("This app is built on the foundational principles of neural style transfer developed by Mr. Shafik Quoraishee, with frontend design by Ms. Manali Jain."),
                    html.H6(["If you wish to join or support the ARTISTvsAI campaign, drop a mail at ",
                        html.A("jmanali1996@gmail.com", href='mailto:jmanali1996@gmail.com', target='_blank')])
                ])
            ])
        ], style={'color': '#000080'})

# IMAGE UPLOAD AND DISPLAY CALLBACK
@app.callback(
    Output('output-image', 'children'),
    Input('upload-image', 'contents')
)
def update_img_output(contents):
    if contents is not None:
        return html.Img(src=contents, style={'maxWidth': '450px', 'maxHeight': '450px'})
    return "No image uploaded yet"

# STYLE UPLOAD AND DISPLAY CALLBACK
@app.callback(
    Output('output-style', 'children'),
    Input('upload-style', 'contents')
)
def update_sty_output(contents):
    if contents is not None:
        return html.Img(src=contents, style={'maxWidth': '450px', 'maxHeight': '450px'})
    return "No style uploaded yet"

# FIRST IMAGE UPLOAD AND DISPLAY CALLBACK
@app.callback(
    Output('output-first-image', 'children'),
    Input('upload-first-image', 'contents')
)
def update_fi_output(contents):
    if contents is not None:
        return html.Img(src=contents, style={'maxWidth': '450px', 'maxHeight': '450px'})
    return "No image uploaded yet"

# SECOND IMAGE UPLOAD AND DISPLAY CALLBACK
@app.callback(
    Output('output-second-image', 'children'),
    Input('upload-second-image', 'contents')
)
def update_si_output(contents):
    if contents is not None:
        return html.Img(src=contents, style={'maxWidth': '450px', 'maxHeight': '450px'})
    return "No image uploaded yet"

# STYLIZE IMAGE CALLBACK
@app.callback(
    Output('stylized-image', 'src'),
    Input('stylize-btn', 'n_clicks'),
    State('upload-image', 'contents'),
    State('upload-style', 'contents')
)
def stylize_image(n_clicks, content_img, style_img):
    if n_clicks is None or content_img is None or style_img is None:
        return None

    content_image_data = content_img.split(',')[1]
    style_image_data = style_img.split(',')[1]

    content_image_decoded = base64.b64decode(content_image_data)
    style_image_decoded = base64.b64decode(style_image_data)

    files = {
        'content_image': content_image_decoded,
        'style_image': style_image_decoded
    }

    response = requests.post(f'{END_POINT}stylize', files=files)

    if response.status_code == 200:
        stylized_image_data = base64.b64encode(response.content).decode('utf-8')
        return 'data:image/png;base64,{}'.format(stylized_image_data)
    else:
        return "Couldn't stylize image"

if __name__ == '__main__':
    app.run_server(debug=True)
