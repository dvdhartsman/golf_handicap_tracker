import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


def add_round(name:str, date:str, adj_gross_score:int, course_rating:np.number, slope_rating:np.number, \
              putts:int, three_putts:int, fairways:int, gir:int, penalties:int, data:pd.DataFrame) -> pd.Series:
    
    """ Given specified input data, a new row will be added to the dataframe

    Args:
    ------------------
    name:str | name of player who's score is being recorded
    date:str | day of the round being recorded
    adj_gross_score:int | total score for the round
    course_rating:np.number | course rating found on the scorecard
    slope_rating:np.number | slope rating found on the scorecard
    putts:int | optional if recorded, the total number of putts
    three_putts:int | optional if recorded, the total number of 3-putts
    fairways:int | options if recorded, the total number of fairways hit on par 4's and par 5's
    gir:int | optional greens in regulation, the total number of gir on all 18 holes
    penalties:int | optional total number of instances of out-of-bounds shots or water penalties
    df:pd.DataFrame | original container of data


    """
    row = {
        "name":name,
        "date":pd.to_datetime(date).normalize(),
        "adj_gross_score":adj_gross_score,
        "course_rating":course_rating,
        "slope_rating":slope_rating,
        "putts": putts,
        "3_putts": three_putts, 
        "fairways_hit": fairways,
        "gir": gir, 
        "penalty/ob": penalties
    }

    row["handicap_diff"] = ((row["adj_gross_score"] - row["course_rating"]) * 113) / row["slope_rating"]
    
    data.loc[len(data)] = row
    
    return df


def get_handicap(data, window=5):

    """
    Return a pd.Series of handicap values based on the window of rounds desired

    Args:
    --------------
    data: pd.DataFrame | dataframe containing all round data filtered by player name
    window: int | number of rounds for which your handicap should be based on

    Returns:
    ---------------
    rolling_means: pd.Series | a Series of values containing the calculated handicap scores
    """

    if window == 5:
        scores = 3
    elif window == 10:
        scores = 5
    else:
        scores = 8
    
    data = data.sort_values(by="date", ascending=True)
    if len(data) < window:
        return pd.Series([None] * len(series), index=data.index)
    rolling_means = data["handicap_diff"].rolling(window).apply(lambda x: x.nsmallest(scores).mean(), raw=False)
    
    return rolling_means


def fill_handicaps(data:pd.DataFrame) -> pd.DataFrame:
    """ Apply the get_handicap() function for each player in the data for 5, 10, and 20 round windows

    Args:
    -----------------
    df: pd.DataFrame | the source of data to be tracked

    Returns:
    -----------------
    df: pd.DataFrame | the supplied dataframe with added columns for each window of handicap
    """

    data = data.sort_values(by="date")
    
    for name in data["name"].unique():
        values = get_handicap(data.loc[data["name"] == name], window=5)
        data.loc[data["name"] == name, "fiveRd_handicap"] = values
    
        data.loc[data["name"] == name, "tenRd_handicap"] = get_handicap(df.loc[df["name"] == name], window=10)
    
        data.loc[data["name"] == name, "twentyRd_handicap"] = get_handicap(df.loc[df["name"] == name], window=20)

    return data
    
        
def plot_statistics(data, column):

    """ Creates a line plot of data tracking the values of a given column over time

    Args:
    ------------------
    data:pd.DataFrame | source of data for the values in the plot
    column:str | name of the column from data to plot

    Returns:
    ------------------
    fig: px.Figure | plotly figure of a lineplot
    """

    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "fiveRd_handicap": "Five-Round Rolling Handicap",
        "tenRd_handicap": "Ten-Round Rolling Handicap",
        "twentyRd_handicap": "Twenty-Round Rolling Handicap"
    }
        
    if len(data.dropna(subset=column)["date"].unique()) < 50:
        length = len(data.dropna(subset=column)["date"].unique()) 
    else:
        length = 50

    date_cutoff = pd.Series(data.dropna(subset=column)["date"].unique()).sort_values().to_list()[-length]
    
    
    fig = px.line(data_frame=data.dropna(subset=column).loc[data["date"] >= date_cutoff],\
                  x="date", y=column, color="name", markers=True, hover_name="name",\
                 title=f"{label_dict[column]}", labels={"date":"Date", column:label_dict[column]},
                 hover_data={"name":False})
    
    fig.update_layout(legend={"title":"Player Name"})

    return fig


def histplot(data:pd.DataFrame, column:str, color_map:dict = {"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}):
    """ Display the distribution of a continuous numeric variable

    Args:
    ----------------
    data:pd.DataFrame | source of data
    column:str | name of the continuous variable to be plotted
    color_map:dict | dictionary of values to ensure color-coding-consistency across plots

    Returns:
    -----------------
    fig:px.Figure | a histogram of the selected continuous variable
    """

    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "fiveRd_handicap": "Five-Round Rolling Handicap",
        "tenRd_handicap": "Ten-Round Rolling Handicap",
        "twentyRd_handicap": "Twenty-Round Rolling Handicap"
    }
    
    fig_h = px.histogram(data, x=column, nbins=len(data[column].unique()), \
                         labels={column:label_dict[column], "count":"Count"}, hover_name="name", color="name", hover_data={"name":True},
                        color_discrete_map=color_map)
    
    
    fig_h.update_layout(yaxis={"title":"Count"}, title=f'Distribution for {label_dict[column]}', barmode="overlay",
                       legend={"title":"Player Name"})
    fig_h.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=.3,
                       hovertemplate=f"<b>%{{fullData.name}}</b><br><br>{label_dict[column]}: %{{x}}<br> No. of Rounds: %{{y}}")
    return fig_h


def pie_chart(data:pd.DataFrame, column:str, player:str=None):
    """
    Pie chart that shows the proportions of fairways hit, gir, 3 putts, penalties - the sub-categories of score

    Args:
    -----------------
    data:pd.DataFrame | source data containing the records of golf rounds
    column:str | name of the metric for which the proportions will be shown
    player:str | name of the player in question

    Returns:
    ------------------
    fig:px.Figure() | a pie chart with a hole in the middle displaying the proportions of values
    """

    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "fiveRd_handicap": "Five-Round Rolling Handicap",
        "tenRd_handicap": "Ten-Round Rolling Handicap",
        "twentyRd_handicap": "Twenty-Round Rolling Handicap"
    }
    
    if player:
        data = data.loc[data["name"] == player]

    fig = px.pie(data_frame=data, names=column, hole=.5, labels={column:label_dict[column]},
                title=f"Proportion of {label_dict[column]}", category_orders={column:[*range(data[column].max().astype(int))]})
    fig.update_layout(legend={"title":player if player else label_dict[column]})
    
    return fig


def dist_plot(data:pd.DataFrame, column:str):
    """
    Function to generate a plotly figure of KDE distributions for selected columns 

    Args
    -----------
    data: pd.DataFrame | data with columns: "name" and continuous variable of interest

    Returns
    -----------
    plotly figure | kde plots overlaid 

    Errors
    -----------
    KeyError if data do not contain the correct columns
    """

    # Create the overlaid plot
    fig = go.Figure()

    colors = ["blue", "red", "green", "orange"]
    
    for i, player in enumerate(data["name"].unique()):
        player_data = data.loc[data["name"]== player][column]

        player_kde = ff.create_distplot([player_data], group_labels=[player], show_hist=False, show_rug=False)
    
        # Player KDE Plot
        fig.add_trace(go.Scatter(x=player_kde['data'][0]['x'], y=player_kde['data'][0]['y'], 
                                 mode='lines', name=player, fill='tozeroy', line=dict(color=colors[i]), opacity=0.9,
                                 hoverinfo='x', xhoverformat=".2f", hovertemplate=f'{column.replace("_", " ").title()}: %{{x:.2f}}'))
    
    # Update layout
    fig.update_layout(height=600, width=800, 
                      title_text=f"{column.replace('_', ' ').title()} Distribution",
                      xaxis_title=f"{column.replace('_', ' ').title()}",
                      yaxis_title="Density",
                      showlegend=True,
                      legend=dict(x=0.875, y=0.875))
    fig.update_yaxes(showticklabels=False)

    return fig


def rolling_avg(data:pd.DataFrame, column:str, window:int, color_map:dict={"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}):
    """
    Function to generate a plotly lineplot of rolling mean column values

    Args:
    -----------
    data: pd.DataFrame | source of data
    column:str | value of interest to find Mean and Median values
    window:int | number of periods for which to find a rolling average
    color_map:dict | dictionary to ensure color-coding-consistency

    Returns
    -----------
    plotly figure | lineplot with hover values of State, Mean/Median Value 

    Errors
    -----------
    KeyError if data do not contain the correct columns
    """

    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "fiveRd_handicap": "Five-Round Rolling Handicap",
        "tenRd_handicap": "Ten-Round Rolling Handicap",
        "twentyRd_handicap": "Twenty-Round Rolling Handicap"
    }

    data = data.set_index("date").sort_index()
    data["rolling_avg"] = data.groupby("name")[column].transform(lambda t: t.rolling(window).mean())
    
    fig = px.line(data_frame = data, y="rolling_avg", color="name", color_discrete_map=color_map, 
                 title=f"{window} Round Rolling Average - {label_dict[column]}", hover_name="name",
                 labels={"rolling_avg":"Rolling Avg", "date":"Date Played"}, hover_data={"name":False})
    fig.update_layout(legend={"title":"Player Name"})
    return fig


def scatter(data:pd.DataFrame, column:str, color_map:dict={"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}, size:str=None,
           jitter_strength=0.25):
    """
    Scatterplot of adjusted gross score on the y-axis vs a selected contributing column on the x-axis

    Args:
    -------------
    data:pd.DataFrame | source of data
    column:str | selected contributing column, i.e. 3-putts, putts, fairways, gir, etc
    color_map:dict | color mapping to ensure color-consistency
    size:str | optional additional contributing column to include more dimensions
    jitter_strenght:float | amount of jitter for the x-axis values

    Returns:
    --------------
    fig:plotly.graph_objects.Figure | scatterplot with color-coded player relationships, options for how to plot additional dimensions
    
    """
    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "fiveRd_handicap": "Five-Round Rolling Handicap",
        "tenRd_handicap": "Ten-Round Rolling Handicap",
        "twentyRd_handicap": "Twenty-Round Rolling Handicap"
    }

    if size:
        title = f"Adj Score vs {label_dict[column]} with {label_dict[size]} as Size<br><sup>X-Jittered for Visibility</sup>"
    else:
        title = f"Adj Score vs {label_dict[column]}<br><sup>X-Jittered for Visibility</sup>"

    data["jittered_col"] = data[column] + np.random.uniform(-jitter_strength, jitter_strength, size=len(df))
    
    fig = px.scatter(data_frame=data, x="jittered_col", y="adj_gross_score", color="name", size=size,
                     hover_name="name", labels={"adj_gross_score":"Adj. Score", "jittered_col":label_dict[column]}, 
                     title = title, hover_data={"name":False, "jittered_col":":.0f"})

    fig.update_layout(legend={"title":"Player Name"}, title={"y":.85})
    fig.update_traces(opacity=.6)
    
    return fig