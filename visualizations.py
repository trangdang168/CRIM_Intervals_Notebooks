import altair as alt
import crim_intervals as ci
import pandas as pd

def plot_ngrams_heatmap(model, mel_ngrams, patterns=[], voices=[]):

    """
    Allowing users to plot a heatmap with a the dataframe returned from getNgrams.
    The users can input a list of specific voices and/or patterns to plot a heatmap. 
    """

    # TODO barplot interactive
        
    # retrieve voices and number of voices before modifying the df
    if not voices:
        voices = mel_ngrams.columns
    num_voices = len(voices)
    
    mel_ngrams_matches_df = pd.DataFrame()

    starts = []
    for i in range(num_voices):
        starts.extend(mel_ngrams.index.astype(float).tolist())
    mel_ngrams_matches_df['start'] = starts


    durations = []
    durations_df = model.getDuration(df=mel_ngrams)
    for voice in voices:
        durations.extend(durations_df[voice])
    mel_ngrams_matches_df['end'] = mel_ngrams_matches_df['start'] + durations
    
    ngrams_patterns = [] # all the patterns that exist in the ngrams df
    for voice in voices:
        ngrams_patterns.extend(mel_ngrams[voice])
    mel_ngrams_matches_df['pattern'] =  ngrams_patterns

    voices_list = [] # store the list of voices to be added to the result df 
    for voice in voices:
        voices_list.extend([voice]*len(mel_ngrams))
    mel_ngrams_matches_df['voices'] = voices_list

    if patterns:
        mel_ngrams_matches_df = mel_ngrams_matches_df[mel_ngrams_matches_df['pattern'].isin(patterns)]
    
    print(mel_ngrams_matches_df)

    observer_selection = alt.selection_multi(fields=['pattern'])
    # brush = alt.observer_selection(type='interval', encodings=['x'])

    chart1 = alt.Chart().mark_bar().encode(
        y='pattern', 
        x='count(pattern)',
        color='pattern',        
        opacity=alt.condition(observer_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        observer_selection
    )


    chart2 = alt.Chart().mark_bar().encode(
        x='start',
        x2='end',
        y='voices',
        color='pattern', 
    ).transform_filter(
        observer_selection
    ).properties(
        width=700,
        height=250
    )

    chart = alt.vconcat(
        chart1, chart2,
        data=mel_ngrams_matches_df.dropna()
    )



    return chart, mel_ngrams_matches_df

def plot_relationship_heatmap(relationship_df, piece_id, heat_map_width=800, heat_map_height=300):

    # filter relationships from one piece
    relationship_df = relationship_df[relationship_df['model_observation.piece.piece_id'] == piece_id]
    relationship_df['location'] = relationship_df['model_observation.ema'].str.split("/", n=1, expand=True)[0]
    relationship_df['location'] = relationship_df['location'].str.split(",")
    relationship_df = relationship_df.explode('location')
    relationship_df[['start', 'end']] = relationship_df['location'].str.split("-", expand=True).fillna(method='ffill', axis=1)
    relationship_df['id'] = relationship_df['id'].astype(str)
    relationship_df['start'] = relationship_df['start'].astype(int)
    relationship_df['end'] = relationship_df['end'].astype(int)

    observer_selection = alt.selection_multi(fields=['observer.name'])
    type_selection = alt.selection_multi(fields=['relationship_type'])

    # plot observers count
    observer_chart = alt.Chart(relationship_df).mark_bar().encode(
        y='observer.name', 
        x='count(observer.name)', 
        color='relationship_type',    
        opacity=alt.condition(observer_selection | type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        observer_selection
    )
    
    # plot relationship count bar plot
    type_chart = alt.Chart(relationship_df).mark_bar().encode(
        y='relationship_type', 
        x='count(relationship_type)',     
        color='relationship_type',  
        opacity=alt.condition(observer_selection| type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        type_selection
    )

    # concat the above two
    heatmap = alt.Chart(relationship_df).mark_bar().encode(
        x='start',
        x2='end',
        y='id',
        color='relationship_type', 
        opacity=alt.condition( observer_selection | type_selection, alt.value(1), alt.value(0.2))
    ).transform_filter(
        observer_selection | type_selection
    ).properties(
        width=heat_map_width,
        height=heat_map_height
    )

    chart = alt.vconcat(
            alt.hconcat(
            observer_chart, type_chart,
        ), heatmap
    )

    # plot the last gantt chart
    return chart, relationship_df
