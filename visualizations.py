import altair as alt
import crim_intervals as ci
import pandas as pd

# TODO pandas training https://youtube.com/playlist?list=PL5-da3qGB5ICCsgW1MxlZ0Hq8LL5U3u9y

# TODO users choosing tables of scores to give patterns 

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
    
    mel_ngrams_matches_df = mel_ngrams.copy()
    mel_ngrams_matches_df.index.name = "start"
    mel_ngrams_matches_df = mel_ngrams_matches_df.reset_index().melt(id_vars=["start"], value_name="pattern", var_name="voices")

    mel_ngrams_matches_df["start"] = mel_ngrams_matches_df["start"].astype(float)
    # TODO currently getDuration is based on index (which is NOT start), causing all patterns to have length of 1
    # durations_df = model.getDuration(df=mel_ngrams_matches_df)
    mel_ngrams_matches_df['end'] = mel_ngrams_matches_df['start'] + 1

    if patterns:
        mel_ngrams_matches_df = mel_ngrams_matches_df[mel_ngrams_matches_df['pattern'].isin(patterns)]
    
    # print(mel_ngrams_matches_df)

    observer_selection = alt.selection_multi(fields=['pattern'])

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
        opacity=alt.condition(observer_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        observer_selection
    )

    chart = alt.vconcat(
        chart1, chart2,
        data=mel_ngrams_matches_df.dropna()
    )

    return chart, mel_ngrams_matches_df


def plot_relationship_heatmap(relationship_df, heat_map_width=800, heat_map_height=300):

    # TODO tooltip, href
    # TODO clean up and abstract

    if len(relationship_df) == 0:
        print("DataFrame is empty!")
        return None, None

    # filter relationships from one piece
    ans_df = relationship_df.copy()
    ans_df['location'] = ans_df['model_observation.ema'].str.split("/", n=1, expand=True).copy()[0]
    ans_df['location'] = ans_df['location'].str.split(",")
    ans_df = ans_df.explode('location')
    # ffill to cover ema locations with only start points, and bfill to cover locations with only end points
    ans_df[['start', 'end']] = ans_df['location'].str.split("-", expand=True).fillna(method='ffill', axis=1)
    ans_df.sort_values(by='id', inplace=True) 
    
    ans_df['id'] = ans_df['id'].astype(str)
    ans_df['start'] = ans_df['start'].astype(float)
    ans_df['end'] = ans_df['end'].astype(float)

    observer_selection = alt.selection_multi(fields=['observer.name'])
    type_selection = alt.selection_multi(fields=['relationship_type'])

    # plot observers count
    observer_chart = alt.Chart(ans_df).mark_bar().encode(
        y='observer.name', 
        x='count(observer.name)', 
        color='relationship_type',    
        opacity=alt.condition(observer_selection | type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        observer_selection
    )
    
    # plot relationship count bar plot
    type_chart = alt.Chart(ans_df).mark_bar().encode(
        y='relationship_type', 
        x='count(relationship_type)',     
        color='relationship_type',  
        opacity=alt.condition(observer_selection| type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        type_selection
    )

    # concat the above two
    heatmap = alt.Chart(ans_df).mark_bar().encode(
        x='start',
        x2='end',
        y='id',
        color='relationship_type', 
        opacity=alt.condition( observer_selection| type_selection, alt.value(1), alt.value(0.2))
    # ).transform_filter(
    #     observer_selection | type_selection
    ).properties(
        width=heat_map_width,
        height=heat_map_height
    ).add_selection(
        type_selection, 
        observer_selection
    )

    chart = alt.vconcat(
            alt.hconcat(
            observer_chart, type_chart,
        ), heatmap
    )

    # plot the last gantt chart
    return chart, ans_df

def plot_observation_heatmap(observation_df, heat_map_width=800, heat_map_height=300):

    if len(observation_df) == 0:
        print("DataFrame is empty!")
        return None, None

    # filter relationships from one piece
    ans_df = observation_df.copy()
    ans_df['location'] = ans_df['ema'].str.split("/", n=1, expand=True).copy()[0]
    ans_df['location'] = ans_df['location'].str.split(",")
    ans_df = ans_df.explode('location')
    # ffill to cover ema locations with only start points, and bfill to cover locations with only end points
    ans_df[['start', 'end']] = ans_df['location'].str.split("-", expand=True).fillna(method='ffill', axis=1)
    ans_df.sort_values(by='id', inplace=True) 
    ans_df['id'] = ans_df['id'].astype(str)
    ans_df['start'] = ans_df['start'].astype(int)
    ans_df['end'] = ans_df['end'].astype(int)

    ans_df = ans_df.rename(columns={"observer.name": "observer_name"})

    observer_selection = alt.selection_multi(fields=['observer_name'])
    type_selection = alt.selection_multi(fields=['musical_type'])

    # plot observers count
    observer_chart = alt.Chart(ans_df).mark_bar().encode(
        y='observer_name', 
        x='count(observer_name)', 
        # color='musical_type',    
        opacity=alt.condition(observer_selection | type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        observer_selection
    )
    
    # # plot relationship count bar plot
    # print(ans_df['observer.name'])
    type_chart = alt.Chart(ans_df).mark_bar().encode(
        y='musical_type', 
        x='count(musical_type)',     
        color='musical_type',  
        opacity=alt.condition(observer_selection| type_selection, alt.value(1), alt.value(0.2))
    ).add_selection(
        type_selection
    )

    # concat the above two
    heatmap = alt.Chart(ans_df).mark_bar().encode(
        x='start',
        x2='end',
        y='id',
        color='musical_type', 
        opacity=alt.condition( observer_selection | type_selection, alt.value(1), alt.value(0.2))
    # ).transform_filter(
    #     observer_selection | type_selection
    ).properties(
        width=heat_map_width,
        height=heat_map_height
    ).add_selection(
        type_selection, 
        observer_selection
    )

    chart = alt.vconcat(
            alt.hconcat(
            observer_chart, type_chart,
        ), heatmap
    )

    # plot the last gantt chart
    return chart, ans_df

# create maps
def create_bar_chart():
    pass

def create_heat_map():
    pass

def process_ngrams_df():
    pass

def from_ema_to_offsets():
    pass
