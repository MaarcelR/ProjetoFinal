import pandas as pd
import locale 
import calendar
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.graph_objects as go
import plotly.express as px
locale.setlocale(locale.LC_TIME,'pt_BR.UTF-8')

df = pd.read_csv('C:/Users/noturno/Desktop/ProjetoFinal/data/df_completo.csv')
df['Total Vendas'] = df['Quantidade'] * df['Preço Unitário']
df['dt_Venda'] = pd.to_datetime(df['dt_Venda'])
# df_meses= df['dt_Venda'].dt.month.unique()
df['Mes'] = df['dt_Venda'].dt.strftime('%b').str.upper() #A maisculo AAAA a minusculo aa (b -- mes abreviado  )
# df_meses_txt = []
# for mes in df_meses:
#     df_meses_txt.append(calendar.month_name[mes])
# df_meses_txt1 = [calendar.month_name[mes] for mes in df_meses] ### outra forma de fazer for...


# listas de meses 
lista_meses=[]
for mes in df['Mes'].unique():  
    lista_meses.append({
        'label': mes,
        'value': mes   
        }
    )
lista_meses.append(
    {'label':'Todos os meses', 'value': 'Ano'}
)

# listas de categorias 
lista_categorias=[]
for categoria in df['Categorias'].unique():  
    lista_categorias.append({
        'label': categoria,
        'value': categoria   
        }
    )

lista_categorias.append(
    {'label':'Todas as Categorias', 'value': 'Categorias'}
)


## lista de clientes
lista_clientes = []

for cliente in df['Cliente'].unique():
    lista_clientes.append(
        {
            'label': cliente.upper(), 
            'value': cliente
        }
    ) 
lista_clientes.append(
    {'label': 'Todos os Clientes', 'value': 'Cliente'}
)
    
#Temas

journal_theme ='journal'
cyborg_theme = 'cyborg'
url_journal_theme = dbc.themes.JOURNAL
url_cyborg_theme = dbc.themes.CYBORG



###-------------------------------------------------------------------------

app = dash.Dash(__name__)

##configuracao do layout da tela  (Div = Criar espaço na tela)
layout_cabecalho = html.Div([
    html.Div(
        html.Legend (
            'Ebony Store ©',
            style={
                'fonte-size': '150%',
                'text-aligm': 'center'
            }
        ),style={'width':'25%'}
    ),
    html.Div(
        dcc.Dropdown(
            id='cliente_dropdown',
            options=lista_clientes,
            placeholder='Escolha um cliente dentro da lista', 
            style={
                'font-family': 'Fira Code',
                'border': 'none',
            }
        ),style={'width':'50%'}
    ),   
    html.Div(
        ThemeSwitchAIO(
            aio_id = 'theme',
            themes=[
                url_journal_theme,
                url_cyborg_theme
            ]
        ),style={'width': '25%'}
    )

],style={
    'text-align':'center',
    'display':'flex',
    'justify-content':'space-arround',
    'margin-top':'20px'
    }
)

 
layout_linha_um= html.Div([
    html.Div([
        html.H4(
            id='output_cliente',
        ),
        dcc.Graph(
            id='visual01'
        )   
    ], style = {
        'text-align':'center',
        'width': '65%'
    }),
    html.Div([
      dbc.RadioItems(
          id='radio_meses',
          options= lista_meses,
          inline=True
      ),
      dbc.RadioItems(
          id='radio_categorias',
          options= lista_categorias,
          inline=True
      )
    ],style= {
        'width': '32%',
        'display': 'flex',
        'flex-direction':'column',
        'justify-content':'space-evenly'
    })
], style= {
    'display':'flex',
    'justify-content':'space-around',
    'margin-top':'20px',
    'height':'300px'
})

layout_linha_dois= html.Div([
    html.Div([
        html.H4('Vendas por Mês e Loja'),
        dcc.Graph(id='visual02')
        ],style={
            'width': '50%',
            'text-align': 'center'
            }
    ), html.Div([
        dcc.Graph(id='visual03') 
        ],style= {
            'width': '35%',
            'text-align': 'center'
            }
        )
],style={
    'display':'flex',
    'justify-content': 'space-around',
    'margin-top':'396px',
    'height':'150px'
})






app.layout = html.Div([
    layout_cabecalho,
    layout_linha_um,
    layout_linha_dois

])


#### ---------------FUNCOES DE APOIO-------------------------####
def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
        return pd.Series(True, index=df.index)
    else:
       return df['Cliente'] == cliente_selecionado

def filtro_mes(mes_selecionado):
    if mes_selecionado is None: 
        return pd.Series(True, index=df.index)
    elif mes_selecionado == 'Ano':
        return pd.Series(True, index=df.index)
    else:
        return df['Mes'] == mes_selecionado

def filtro_categoria(categoria_selecionada):
    if categoria_selecionada is None:
        return pd.Series(True, index=df.index)
    elif categoria_selecionada == 'Categorias':
        return pd.Series(True, index=df.index)
    else:
        return df['Categorias'] == categoria_selecionada





#### ---------------------CALLBACKS------------------------------
# ela é chamada por um evento que acontece
# para funções ela tem que ser chamada.
#### ---------------------CALLBACKS------------------------------

@app.callback(
    Output ('output_cliente', 'children'),
    Input('cliente_dropdown','value')
)
def output_update(cliente_selecionado):
    if cliente_selecionado:
        return f'Top 5 produtos comprados por: {cliente_selecionado}'
    return 'Top 5 produtos vendidos'


@app.callback(
    Output('visual01','figure'), # quando é grafico, necessariamente deve ser uma figura
    [   
        Input('cliente_dropdown','value'),
        Input('radio_meses','value'),
        Input('radio_categorias','value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]

)
def visual01(cliente, mes, categorias, toggle):
    template = cyborg_theme if toggle else journal_theme

    nome_cliente = filtro_cliente(cliente)
    nome_mes = filtro_mes(mes)
    nome_categoria = filtro_categoria(categorias)
    cliente_mes_categoria = nome_cliente & nome_mes & nome_categoria

    df1 = df.loc[cliente_mes_categoria]
    

    print(df1)
    # Manipulacao de dados
    df_grupo = df1.groupby(
        ['Produto',
         'Categorias'])['Total Vendas'].sum().reset_index()
    df_top5 = df_grupo.sort_values(
        by='Total Vendas', 
        ascending=False).head(5)
   # criando grafico
    fig1 = px.bar(
        df_top5,
        x='Produto',
        y= 'Total Vendas',
        text='Total Vendas',
        color= 'Total Vendas',
        color_continuous_scale='blues',
        height= 650,
        template = template,
    )
    fig1.update_traces(
        texttemplate='%{text:.2s}',
        textposition='outside',
        )
    fig1.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=False,
            range=[
                df_top5['Total Vendas'].min() * 0,
                df_top5['Total Vendas'].max() * 1.2
            ]
        ),
        xaxis_title=None,
        yaxis_title=None,
        xaxis_tickangle=-15,
        margin=dict(t=0),
        font=dict(size=17),
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)'
    )

    return fig1
 

@app.callback(
    [
    Output('visual02','figure'), # quando é grafico, necessariamente deve ser uma figura
    Output('visual03','figure')   
    ],
    [   
        Input('radio_meses','value'),
        Input('radio_categorias','value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)
def visual02(mes, categoria, toggle):
    template = cyborg_theme if toggle else journal_theme

    nome_mes = filtro_mes(mes)
    nome_categoria = filtro_categoria(categoria)
    mes_categoria = nome_mes & nome_categoria
    
    df2 = df.loc[nome_categoria]
    df3 = df.loc[mes_categoria]

    df_vendas_loja = df2.groupby(['Mes', 'Loja'])['Total Vendas'].sum().reset_index()

    df_vendas_loja1 = df3.groupby(['Mes', 'Loja'])['Total Vendas'].sum().reset_index()
    # print(df_vendas_loja)

    max_size = df_vendas_loja['Total Vendas'].max()
    min_size = df_vendas_loja['Total Vendas'].min()

    cores_lojas={
        'Rio de Janeiro': '#0000CD'
        ,'São Paulo': '#FFA500'
        ,'Salvador': '#FFFF00'
        ,'Santos': '#FF8C00'
        # ,'Três Rios':'#4169E1'
    }
    meses = [
        'JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
        'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'
    ]        

    # Criação do Gráfico
    fig2 = go.Figure()
    for loja in df_vendas_loja['Loja'].unique():
        df_loja = df_vendas_loja[df_vendas_loja['Loja'] == loja]
        cor = cores_lojas.get(loja, 'Black')    
        fig2.add_trace(
            go.Scatter(
                x=df_loja['Mes'],
                y=df_loja['Total Vendas'],
                mode='markers',
                marker=dict(
                    size=(df_loja['Total Vendas']-min_size) /
                    (max_size - min_size) * 50
                ),
                opacity=0.5,
                line=dict(color=cor, width=0),
                name=str(loja)
            )
        )

        fig2.update_layout(
            margin=dict(t=0),
            template = template,
            # font=dict(size=17),
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            xaxis= dict(
                showgrid=False,
                categoryorder='array',
                categoryarray=meses
                ),
            yaxis= dict(showgrid=False),
            
        )
    # Criação do Gráfico
    fig3 = go.Figure(
        data=go.Scatterpolar(
            r=df_vendas_loja1['Total Vendas'],
            theta=df_vendas_loja1['Loja'],
            line=dict(color='orange'), #line=dict(color='rgb(31,119,180)')
            marker=dict(color='rgb(31,119,80)',size=10),
            opacity=0.5
        )
    )
    fig3.update_layout(
        template = template,
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickfont=dict(
                    size=13, color='pink'
                    ),
                tickangle=0,
                ticklen=5,
                range=[
                    0,
                    max(df_vendas_loja1['Total Vendas']) + 1000
                    ]
            )
        ),
        font=dict(
            family='Fira Code', 
            size=18
        ), 
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        margin=dict(
            l=30, # esquerda
            r=30, # direita
            t=30, # topo
            b=30  # fundo
        )
    )

    return fig2,fig3        












if __name__ == '__main__':
    app.run_server(debug=True)



