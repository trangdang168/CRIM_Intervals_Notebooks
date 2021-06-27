import requests
import pandas as pd
from pandas.io.json import json_normalize
import altair as alt # visualization library; see https://altair-viz.github.io/
import old_visualizations as viz

data_relationships = requests.get('http://crimproject.org/data/relationships/').json()
#df = pd.DataFrame(data)
df_relationships = pd.json_normalize(data_relationships)
pieces = df_relationships['model_observation.piece.piece_id'].unique()

chart, df = viz.plot_relationship_heatmap(df_relationships, 'CRIM_Model_0008')
print(df)