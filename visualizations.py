import altair as alt
import crim_intervals as ci
import pandas as pd

def plot_ngrams_heatmap(mel_ngrams, patterns=[], voices=[]):

    # TODO error, not work with harmonic or melodic

    """
    Allowing users to plot a heatmap with a the dataframe returned from getNgrams.
    The users can input a list of specific voices and/or patterns to plot a heatmap. 
    """
        
    # retrieve voices and number of voices before modifying the df
    if not voices:
        voices = mel_ngrams.columns
    num_voices = len(voices)
    
    mel_ngrams_matches_df = pd.DataFrame()

    starts = []
    for i in range(num_voices):
        starts.extend(mel_ngrams.index.astype(float).tolist())
    # TODO sometimes starts has patterns
    mel_ngrams_matches_df['start'] = starts
    mel_ngrams_matches_df['end'] = mel_ngrams_matches_df['start'].shift(periods=-1)
    
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

    chart = alt.Chart(mel_ngrams_matches_df.dropna()).mark_bar().encode(
    x='start',
    x2='end',
    y='voices',
    color='pattern'
    )
    
    return chart