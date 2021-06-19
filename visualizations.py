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
    
    # print(mel_ngrams_matches_df.dtypes)

    selection = alt.selection_multi(fields=['pattern'])
    # brush = alt.selection(type='interval', encodings=['x'])

    chart1 = alt.Chart().mark_bar().encode(
        x='pattern', 
        y='count(pattern)',
        color='pattern',        
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        selection
    )


    chart2 = alt.Chart().mark_bar().encode(
        x='start',
        x2='end',
        y='voices',
        color='pattern', 
    ).transform_filter(
        selection
    ).properties(
        width=700,
        height=250
    )

    chart = alt.vconcat(
        chart1, chart2,
        data=mel_ngrams_matches_df.dropna()
    )



    return chart, mel_ngrams_matches_df