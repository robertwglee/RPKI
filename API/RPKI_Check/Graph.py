import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from datetime import date
import os
if not os.path.exists("images"):
    os.mkdir("images")
import config


today = date.today()
graph_title =  (config.message) + str(today)
print(graph_title)
csvfile = (config.filepath)
df = pd.read_csv(csvfile, sep = ",")
dfg=df.groupby('RPKI_Status').count().reset_index()
dfg=dfg.rename(columns={"ASN": "ASN"})

fig = px.pie(dfg,
             names ='RPKI_Status',
             values ='ASN',
             #x='RPKI_Status',
             #y='ASN',
             title=(graph_title),
             color='RPKI_Status',
             color_discrete_map={'VALID':'mediumseagreen','UNKNOWN':'lightgray', 'INVALID':'red'},
             #barmode='stack',
             labels={'RPKI_Status': 'RPKI Status', 'ASN':'AS812 Advertised Routes'})
fig.update_traces(textposition='inside', textinfo='value+label')
# Bar Graph
# fig = px.bar(dfg,
#              x='RPKI_Status',
#              y='ASN',
#              title='RPKI Status Check',
#              color='RPKI_Status',
#              barmode='stack',
#              labels={'RPKI_Status': 'RPKI Status', 'ASN':'AS812 Advertised Routes'}
#              )
# fig.update_traces(marker_color='aquamarine')
# plot
fig.show()
fig.write_image("images/fig1.png")