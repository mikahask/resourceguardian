import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import PyPDF2
import base64
import io
import os
import uuid

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("PDF Text Extractor"), className="text-center my-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-pdf',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a PDF File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output-text', className="mt-4"), width=12)
    ])
])

def extract_text_from_pdf(file_content):
    text = ""
    pdf_file = io.BytesIO(file_content)
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

@app.callback(
    Output('output-text', 'children'),
    Input('upload-pdf', 'contents'),
    State('upload-pdf', 'filename')
)
def update_output(file_contents, filename):
    if file_contents is not None:
        content_type, content_string = file_contents.split(',')
        decoded = base64.b64decode(content_string)
        text = extract_text_from_pdf(decoded)
        return html.Pre(text)
    return "No file uploaded yet."

if __name__ == "__main__":
    app.run_server(debug=True)