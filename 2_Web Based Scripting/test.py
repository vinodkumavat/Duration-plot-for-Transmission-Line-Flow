import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import calendar
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
app.css.config.serve_locally = True

# extracting the main data
df = pd.read_excel(r'Lines_Plot.xlsx')
months=df['time'].dt.month.unique()[:-1]

# reading the Station name and there id excel file
mapping_df = pd.read_excel(r'Station_Name_Id.xlsx')

# getting station name from station id
def line_name(line):
    try:
        return mapping_df[mapping_df['Station ICT ID']==line]['Station Name'].values[0]
    except:
        return line



# creating drop down menu
dropdown_options = df.columns.tolist()[1:]



# deriving the x_axis values
def deriveDurationVals(data):
    vals = np.array(data)
    min_value = vals.min()
    max_value = vals.max()+0.0000001
    resol=(max_value-min_value)/1000 
    binVals = []
    perc_time_exceeded = []
    numVals = len(vals)    
    for val in np.arange(min_value,max_value,resol):
        binVals.append(val)
        perc_exceeded = len(vals[vals>val])*100/numVals
        perc_time_exceeded.append(perc_exceeded)
    return perc_time_exceeded, binVals



# plotting the graph for 3 months
def plot_for_month(line,ref):
    figure={'data':[],'layout':[]}
    display_text=''
    for month in months:
        data=df[df['time'].dt.month==month][line]

        perc_time_exceeded,binVals= deriveDurationVals(data)
        Vals= np.array(data)
        perc_exceeded = len(Vals[Vals>float(ref)])*100/len(Vals)

        figure['data'].append({'x':perc_time_exceeded,'y':binVals, 'type': 'scatter','name':calendar.month_name[month]})

        display_text+=f'{calendar.month_name[month]} = {round(perc_exceeded,2)}, '
    figure['data'].append({'x':perc_time_exceeded, 'y':len(perc_time_exceeded)*[ref], 'type': 'scatter',
                 'line':{'color':'black','width':2.4},'name':'ref'})
    



    layout={'title':line_name(line),
     'xaxis':{'title':'% Time Duration'},
     'yaxis':{'title':'Load (Mega Watt)'},
     'height':600
     }
    figure['layout']=layout
    fig=dcc.Graph(
        id='example-graph',
        figure= figure,
        config={'editable':True})
    
    return fig, display_text



# creating drop down menu and reference input box also the graph
app.layout =html.Div([
        html.Div([
        dcc.Dropdown(
     id='State-dropdown',
            options=[{'label':str(i)+'. '+ line_name(line),
                      'value':line} for i,line in enumerate(dropdown_options)],
            value = dropdown_options[0]),
            ],style={'width': '40%', 'display': 'inline-block'}),
  
    dcc.Input(
                    id="Ref_input",
                    value=0,
                    placeholder="Reference_Input",
                ),
            html.Div(id='my-graph'),
            html.Div(id='displaytext',style={'text-align':'center'}),
])



# calling functions to plot graph and display the other stuff
@app.callback(
    [dash.dependencies.Output('my-graph', 'children'),
    dash.dependencies.Output('displaytext', 'children')],
    [dash.dependencies.Input('State-dropdown', 'value'),
    dash.dependencies.Input('Ref_input', 'value')])



# updating the graph
def update_graph(line,ref):
    plot, display_text = plot_for_month(line,ref)
    return [plot], display_text
      


if __name__ == '__main__':
    app.run_server(debug=False,host= '0.0.0.0',port='8080') 