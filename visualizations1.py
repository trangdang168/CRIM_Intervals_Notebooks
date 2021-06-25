import altair as alt

def create_bar_chart(x, y, color, data, condition, *selectors):
    observer_chart = alt.Chart(data).mark_bar().encode(
        y=y, 
        x=x, 
        color = color,    
        opacity=alt.condition(condition, alt.value(1), alt.value(0.2))
    ).add_selection(
        *selectors
    )
    return observer_chart

def create_heatmap(x, x2, y, color, data, heat_map_width, heat_map_height, selector_condition, *selectors):

    heatmap = alt.Chart(data).mark_bar().encode(
        x=x,
        x2=x2,
        y=y,
        color=color, 
        opacity=alt.condition(selector_condition, alt.value(1), alt.value(0.2))
    ).properties(
        width=heat_map_width,
        height=heat_map_height
    ).add_selection(
        *selectors
    )

    return heatmap

def process_ngrams_df(ngrams_df, model=None, selected_pattern = [], voices = []):
    """
    This method combines ngrams from all voices in different columns
    into one column and calculates the starts and end points of the
    patterns. It could also filter out specific voices or patterns
    for the users to analyze.

    :param ngrams_df: dataframe we got from getNgram in crim-interval
    :param model: if not None, rely on the model to calculate the durations of patterns 
    of just outputing only offsets (default=False).
    :param selected_pattern: list of specific patterns the users want (optional)
    :param voices: list of specific voices the users want (optional)
    :return: a processed dataframe with only desired patterns from desired voices
    combined into one column with start and end points
    """

    # copy to avoid changing original ngrams df
    ngrams_df = ngrams_df.copy()

    # add a start column containing offsets
    ngrams_df.index.name = "start"
    ngrams_df = ngrams_df.reset_index().melt(id_vars=["start"], value_name="pattern", var_name="voice")

    ngrams_df["start"] = ngrams_df["start"].astype(float)

    # TODO add durations when getDuration is fixed
    if model:
        durations_df = model.getDuration(df=ngrams_df)
        ngrams_df['end'] = ngrams_df['start'] + durations_df['pattern']
    else:
        # currently, make end=start+1 just to display offsets
        ngrams_df['end'] = ngrams_df['start'] + 1

    # filter according to voices and patterns (after computing durations for correct offsets)
    if voices:
        voice_condition = ngrams_df['voice'].isin(voices)
        ngrams_df = ngrams_df[voice_condition].dropna(how='all')
    
    if selected_pattern:
        pattern_condition = ngrams_df['pattern'].isin(selected_pattern)
        ngrams_df = ngrams_df[pattern_condition].dropna(how='all')

    return ngrams_df

def plot_ngrams_df_heatmap(processed_ngrams_df, selected_pattern = [], voices = [], heatmap_width=800, heatmap_height=300):
    """
    Plot a heatmap for crim-intervals getNgram's output.
    :param ngrams_df: processed crim-intervals getNgram's output.
    :param selected_pattern: list of specific patterns the users want (optional)
    :param voices: list of specific voices the users want (optional)
    :param heatmap_width: the width of the final heatmap (optional)
    :param heatmap_height: the height of the final heatmap (optional)
    :return: a bar chart that displays the different patterns and their counts,
    and a heatmap with the start offsets of chosen voices / patterns
    """

    processed_ngrams_df = processed_ngrams_df.dropna(how='any')
    
    selector = alt.selection_multi(fields=['pattern'])
    patterns_bar = create_bar_chart('pattern', 'count(pattern)', 'pattern', \
                                    processed_ngrams_df, selector, selector)
    heatmap = create_heatmap('start', 'end', 'voice', 'pattern', processed_ngrams_df,\
                             heatmap_width, heatmap_height, selector, selector)
    return alt.vconcat(patterns_bar, heatmap), processed_ngrams_df

def plot_ngrams_heatmap(ngrams_df, model=None, selected_pattern = [], voices = [], heatmap_width=800, heatmap_height=300):
    processed_ngrams_df = process_ngrams_df(ngrams_df, model=None, selected_pattern=selected_pattern, voices=voices)
    return plot_ngrams_df_heatmap(processed_ngrams_df, selected_pattern = selected_pattern, voices = voices, \
                            heatmap_width=heatmap_width, heatmap_height=heatmap_height)

def from_ema_to_offsets(df, ema_column):
    """
    This method adds a columns of start and end measure of patterns into
    the relationship dataframe using the column with the ema address.

    :param df: dataframe containing relationships between patterns retrieved
    from CRIM relationship json
    :param ema_column: the name of the column storing ema address.
    :return: the processed dataframe with two new columns start and end
    """
    # retrieve the measures from ema address and create start and end in place
    df['locations'] = df[ema_column].str.split("/", n=1, expand=True)[0]
    df['locations'] = df['locations'].str.split(",")
    df = df.explode('locations')
    df[['start', 'end']] = df['locations'].str.split("-", expand=True)
    
    # convert to float in case measures are fractions
    df['start'] = df['start'].astype(float)
    df['end'] = df['end'].astype(float)
    return df


def plot_relationship_heatmap(df, ema_col, category1='musical_type', category0='observer.name', option=1, heat_map_width=800,
                              heat_map_height=300):
    """
    This method plots a chart relationships/observations dataframe retrieved from their
    corresponding json files. This chart has two bar charts displaying the count of variables
    the users selected, and a heatmap displaying the locations of the relationship.
    :param df: relationships or observations dataframe
    :param ema_col: name of the ema column
    :param category1: name of the first category for the first bar chart.
    (default='musical_type')
    :param category0: name of the zeroth category for the zeroth bar chart.
    (default='observer.name')
    :param option: if 0, the charts would be colored based on category0,
    if 1, all of the charts would be colored based on category1. (default=1)
    :param heatmap_width: the width of the final heatmap (default=800)
    :param heatmap_height: the height of the final heatmap (default =300)
    :return: a big chart containing two smaller bar chart and a heatmap
    """

    df = df.copy()  # create a deep copy of the selected observations to protect the original dataframe
    df = from_ema_to_offsets(df, ema_col)

    # sort by id
    df.sort_values(by='id', inplace=True)

    df = from_ema_to_offsets(df, ema_col)

    df['id'] = df['id'].astype(str)

    # because altair doesn't work when the categories' names have periods,
    # a period is replaced with a hyphen.

    new_category0 = category0.replace(".", "_")
    new_category1 = category1.replace(".", "_")

    df.rename(columns={category0: new_category0, category1:new_category1}, inplace=True)

    selector1 = alt.selection_multi(fields=[new_category0])
    selector0 = alt.selection_multi(fields=[new_category1])

    if option:
        color = new_category1
        main_selector = selector1
    else:
        color = new_category0
        main_selector = selector0

    bar1 = create_bar_chart(new_category1, str('count(' + new_category1 + ')'), \
                               color, df, selector1 | selector0, selector0)
    bar0 = create_bar_chart(new_category0, str('count(' + new_category0 + ')'), \
                                color, df, selector1 | selector0, selector1)

    heatmap = create_heatmap('start', 'end', 'id', color, df, 800, 300, selector1 | selector0, main_selector)

    chart = alt.vconcat(
        alt.hconcat(
            bar1,
            bar0
        ),
        heatmap
    )

    return chart, df



