import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Cargamos y preparamos los datos.
data = pd.read_csv('C:/Users/rodri/OneDrive/Escritorio/Trabajos/Análisis de datos/supermarket_sales - Sheet1.csv')
data['Date'] = pd.to_datetime(data['Date'])
gross_income_per_branch = data.groupby('Branch')['gross income'].sum()
payment_method_counts = data['Payment'].value_counts()
gross_income_per_date = data.groupby('Date')['gross income'].sum()

# Paleta de colores.
paleta = ['#355070', '#6d597a', '#b56576', '#e56b6f', '#eaac8b']
px.defaults.color_discrete_sequence = paleta

# Inicializamos la aplicación Dash.
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

app.layout = html.Div(children=[
    html.H1(children='Proyecto: Análisis de Supermercados', className='text-center mb-4'),

    html.Div(children='Visualización de datos de los supermercados.', className='text-center mb-4'),

    # Gráfico 'Sucursal con más ingresos brutos'
    html.Div([
        html.Div([
            dcc.Graph(
                figure=px.bar(gross_income_per_branch,
                              x=gross_income_per_branch.index,
                              y=gross_income_per_branch.values)
                              .update_layout(title_text='Sucursal con más ingresos brutos',
                                             xaxis_title='Sucursal',
                                             yaxis_title='Ingresos Brutos')
            )
        ], className='col-lg-6'),

        # Gráfico 'Forma de pago más usadas'
        html.Div([
            dcc.Graph(
                id='payment-method-distribution',
                figure=px.pie(payment_method_counts,
                              names=payment_method_counts.index,
                              values=payment_method_counts.values,
                              title='Formas de pago más usadas.')
                  .update_layout(showlegend=False) 
            )
        ], className='col-lg-6')
    ], className='row'),

    # Gráfico 'Ingresos brutos diarios'
    html.Div([
        dcc.Graph(
            figure=px.line(gross_income_per_date,
                           x=gross_income_per_date.index,
                           y=gross_income_per_date.values)
                           .update_layout(title_text='Ingresos brutos diarios',
                                          xaxis_title='Fecha',
                                          yaxis_title='Ingresos Brutos Totales')
        )
    ], className='col-12 mt-4')
], className='container-fluid')

if __name__ == '__main__':
    app.run_server(debug=True)
