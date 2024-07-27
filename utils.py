import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff



label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format",
        "golf_course":"Golf Course",
        "oppenent_s":"Opponent/s",
        "notes":"Notes"
    }


def add_round(name:str, date:str, adj_gross_score:int, course_rating:float, slope_rating:float,
              putts:int=np.nan, three_putts:int=np.nan, fairways:int=np.nan, gir:int=np.nan, penalties:int=np.nan, birdies:int=np.nan,
              trpl_bogeys_plus:int=np.nan, profit_loss:float=np.nan, match_format:str=np.nan,
              golf_course:str=np.nan, opponent_s:str=np.nan, notes:str=np.nan, calc_diff:bool=True) -> pd.Series:

    
    
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
    birdies:int | number of birdies (one-under on a hole) in a round
    trpl_bogeys_plus:int | number of holes with scores worse than a double bogey
    profit_loss:float | number of betting units won or lost in a competition round
    match_format:str | type of competition
    golf_course:str | name of course played at
    opponent_s:str | name of opponent/s for the round
    calc_diff:bool | whether or not to calculate the handicap differential on the spot, could be deferred to perform vectorization if MANY rows
                        are being entered simultaneously

    Returns:
    ------------------
    row:pd.Series | row of data for a new round
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
        "penalty/ob": penalties,
        "birdies":birdies,
        "trpl_bogeys_plus":trpl_bogeys_plus,
        "profit/loss":profit_loss,
        "match_format":match_format,
        "golf_course":golf_course,
        "opponent/s":opponent_s,
        }

    if calc_diff:
        row["handicap_diff"] = ((row["adj_gross_score"] - row["course_rating"]) * 113) / row["slope_rating"]
    
    return row


# Perform handicap diff calculation on whole dataframe
def handicap_differentials(data:pd.DataFrame) -> pd.Series:
    """
    apply the handicap differential calculation for each round of golf entered

    Args:
    -------------
    data:pd.DataFrame | source of data

    Returns:
    -------------
    pd.Series | series of handicap differential values
    """
    return ((data["adj_gross_score"] - data["course_rating"]) * 113) / data["slope_rating"]


# Loop to create fake data
def generate_data(data:pd.DataFrame, player_list:list=["Pete", "Dave", "Eric", "Fred", "Doc"], start_date:pd.Timestamp=pd.Timestamp.today()):
    """
    Create synthetic data for demonstration purposes and add it to data in place
    
    Args:
    --------------
    data:pd.DataFrame | dataframe to add synthetic data to
    player_list:list | list of names to generate synthetic data for
    start_date:pd.Timestamp | date to use as the earliest date for the synthetic data 

    Returns:
    --------------
    None: | the function updates the data argument in place

    """
    today = start_date
    
    for n in player_list:
        # Populate the fields for the add_round() call
        avg_score = np.random.randint(low=80, high=90)
        avg_putts = np.random.randint(low=18, high=54)
        avg_three_putts = np.random.randint(low=0, high=10)
        avg_fairways = np.random.randint(low=1, high=14)
        avg_gir = np.random.randint(low=0, high=18)
        avg_penalities = np.random.randint(low=0, high=10)
        avg_birdies = np.random.randint(low=0, high=2)
        avg_trpl_plus = np.random.randint(low=0, high=3)
        avg_profit_loss = np.random.choice([*np.arange(-1, 1.5, .5)])
        
        for i in range(100):
            name = n
            date = today + pd.Timedelta(days=i * np.random.choice([2,3]))
            adj_gross_score = int(max(np.random.normal(loc=avg_score, scale=5, size=1), 72))
            course_rating = float(np.random.choice([71, 71.5, 72, 72.5, 73, 73.5]))
            slope_rating = int(np.random.randint(low=110, high=130, size=1))
            putts = int(max(np.random.normal(loc=avg_putts, scale=5, size=1), 0))
            if putts > 54:
                putts = 54
            elif putts < 18:
                putts = 18
            three_putts = int(max(np.random.normal(loc=avg_three_putts, scale = 1, size = 1), 0))
            if three_putts > 18:
                three_putts = 18
            elif three_putts <= 0:
                three_putts = 0
            fairways = int(max(np.random.normal(loc=avg_fairways, scale = 2, size = 1),0))
            if fairways > 18:
                fairways = 18
            elif fairways <= 0:
                fairways = 0
            gir = int(max(np.random.normal(loc=avg_gir, scale = 2, size = 1),0))
            if gir > 18:
                gir = 18
            elif gir <= 0:
                gir = 0
            penalties = int(max(np.random.normal(loc=avg_penalities, scale = 2, size = 1),0))
            birdies = int(max(np.random.normal(loc=avg_birdies, scale = 1, size = 1),0))
            trpl_bogeys = int(max(np.random.normal(loc=avg_dbl_plus, scale = 1, size = 1),0))
            profit_loss = round(float(np.random.normal(loc=avg_profit_loss, scale = 2, size = 1)) * 2) / 2 
            match_format = np.random.choice(["Skins", "Match Play", "Stroke Play", "Dots"])
            golf_course = np.random.choice(["Augusta National", "Pebble Beach", "Bethpage Black", "Kiawah Island", "Whistling Straits",
                                            "Pinehurst", "Hollybrook", "Harbortown"])
            opponent_s = np.random.choice([i for i in player_list if i != n])
            notes = np.random.choice(["I played well", "I played badly", "I got lucky", "I got unlucky", "The golf Gods hate me"])

            
        
            # Call function and add to the df
            data.loc[len(data)] = add_round(name=name, date=date, adj_gross_score=adj_gross_score, course_rating=course_rating, 
                                            slope_rating=slope_rating, putts=putts,
                                            three_putts=three_putts, fairways=fairways, gir=gir, penalties=penalties, birdies=birdies, 
                                            trpl_bogeys_plus=trpl_bogeys, profit_loss=profit_loss, match_format=match_format,
                                            golf_course=golf_course, opponent_s=opponent_s, notes=notes,
                                            calc_diff=False)  
            # calc_diff = False to save on computational resources by performing vector op



def get_handicaps(data:pd.DataFrame):
    """
    Get handicap values for each player in the data based on the required logic/calculations

    Args:
    -----------------
    data:pd.DataFrame | source of data

    Returns:
    -----------------
    data:pd.DataFrame | updated data with new handicap column
    """

    # Sort the DataFrame by date
    data = data.sort_values(by="date")
    
    # Initialize the handicap column
    data['handicap'] = np.nan
    
    # Process each player individually
    for player in data["name"].unique():
        player_df = data.loc[data["name"] == player].reset_index(drop=True)
        
        for i, row in player_df.iterrows():
            if i < 2:
                player_df.loc[i, "handicap"] = np.nan
            elif i == 2:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].min() * 0.96 - 2
            elif i == 3:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].min() * 0.96 - 1
            elif i == 4:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].min() * 0.96
            elif i == 5:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(2).mean() * 0.96 - 1
            elif 6 <= i <= 7:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(2).mean() * 0.96
            elif 8 <= i <= 10:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(3).mean() * 0.96
            elif 11 <= i <= 13:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(4).mean() * 0.96
            elif 14 <= i <= 15:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(5).mean() * 0.96
            elif 16 <= i <= 17:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(6).mean() * 0.96
            elif i == 18:
                player_df.loc[i, "handicap"] = player_df.loc[:i, "handicap_diff"].nsmallest(7).mean() * 0.96
            elif i >= 19:
                player_df.loc[i, "handicap"] = player_df.loc[i-20:i, "handicap_diff"].nsmallest(8).mean() * 0.96
        
        # Update the main DataFrame with the calculated handicaps
        data.loc[data["name"] == player, "handicap"] = player_df["handicap"].values

    return data


# Dead function
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
    
        data.loc[data["name"] == name, "tenRd_handicap"] = get_handicap(data.loc[data["name"] == name], window=10)
    
        data.loc[data["name"] == name, "twentyRd_handicap"] = get_handicap(data.loc[data["name"] == name], window=20)

    return data
    
        
def plot_statistics(data, column, color_map:dict = {"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}):

    """ Creates a line plot of data tracking the values of a given column over time

    Args:
    ------------------
    data:pd.DataFrame | source of data for the values in the plot
    column:str | name of the column from data to plot
    color_map:dict | dictionary of values to ensure color-coding-consistency across plots

    Returns:
    ------------------
    fig: px.Figure | plotly figure of a lineplot
    """

    # label_dict = {
    #     "adj_gross_score":"Adjusted Gross Score", 
    #     "handicap_diff": "Handicap Differential",
    #     "putts": "Putts per Round",
    #     "3_putts": "3-Putts per Round",
    #     "fairways_hit": "Fairways Hit per Round",
    #     "gir": "Greens in Regulation",
    #     "penalty/ob": "Penalties / OB per Round",
    #     "handicap":"Handicap Index",
    #     "birdies":"Birdies",
    #     "dbl_bogeys_plus":"Double Bogey or Worse",
    #     "profit/loss":"Profit/Loss",
    #     "match_format":"Match Format"
    # }
        
    # if len(data.dropna(subset=column)["date"].unique()) < 50:
    #     length = len(data.dropna(subset=column)["date"].unique()) 
    # else:
    #     length = 50

    # date_cutoff = pd.Series(data.dropna(subset=column)["date"].unique()).sort_values().to_list()[-length]
    
    # .loc[data["date"] >= date_cutoff]
    
    fig = px.line(data_frame=data.dropna(subset=column),\
                  x="date", y=column, color="name", color_discrete_map=color_map, markers=True, hover_name="name",\
                 title=f"{label_dict[column]} Over Time", labels={"date":"Date", column:label_dict[column]},
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
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }
    
    fig_h = px.histogram(data, x=column, nbins=len(data[column].unique()), \
                         labels={column:label_dict[column], "count":"Count"}, hover_name="name", color="name", hover_data={"name":True},
                        color_discrete_map=color_map, marginal="box")
    
    
    fig_h.update_layout(yaxis={"title":"Count"}, title=f'Distribution for {label_dict[column]}<br><sup>Boxplots Show Additional Distribution Detail</sup>', barmode="overlay",
                       legend={"title":"Player Name"})
    fig_h.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=.45,
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
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }
    
    if player:
        data = data.loc[data["name"] == player]

    fig = px.pie(data_frame=data, names=column, hole=.5, labels={column:label_dict[column]},
                title=f"{player}'s Proportion of {label_dict[column]}", category_orders={column:[*range(data[column].max().astype(int))]})
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

    colors = px.colors.qualitative.Vivid
    
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


def mean_med_stats(data:pd.DataFrame, column:str, color_map:dict={"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}):
    """
    Function to generate a plotly barplots of mean and median column values

    Args:
    -----------
    data: pd.DataFrame | source of data
    column:str | value of interest to find Mean and Median values
    color_map:dict | dictionary to ensure color-coding-consistency

    Returns
    -----------
    plotly figure | barplot with Mean/Median/Stddev Values 

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
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }
    
    # Grouping data by state and calculating median and mean
    grouped = data.groupby("name")[column].agg(["median", "mean","std"]).sort_values(by="median", ascending=False)

    # Resetting index to make 'state' a column for Plotly
    grouped = grouped.reset_index().rename(columns={"median":"Median", "mean":"Average", "std":"Standard Deviation"})

    # Creating Plotly figure
    fig = px.bar(grouped, x='name', y=['Median', 'Average', "Standard Deviation"],
                 labels={'value': label_dict[column], 'name': 'Player Name', "variable":"Statistic"},
                 title=f'Mean and Median {label_dict[column]}<br><sup>Aggregate Statistics for Each Player</sup>', hover_name="name",
                 hover_data={"name":False},
                 template="seaborn", 
                barmode='group')
    
    # Legend/layout
    fig.update_layout(legend_title='Statistics', title={"x":0, "y":.85,})

    fig.for_each_trace(lambda t: t.update(name=t.name.capitalize()))
    fig.update_layout(yaxis=dict(tickformat='.2f'))
    # Returning the Plotly figure
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
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }

    data = data.set_index("date").sort_index()
    data["rolling_avg"] = data.groupby("name")[column].transform(lambda t: t.rolling(window).mean())
    
    fig = px.line(data_frame = data.dropna(subset="rolling_avg"), y="rolling_avg", color="name", color_discrete_map=color_map, 
                 title=f"{window} Round Rolling Average - {label_dict[column]}", hover_name="name",
                 labels={"rolling_avg":"Rolling Avg", "date":"Date Played"}, hover_data={"name":False}, markers=True)
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
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double Bogey or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }

    if size:
        title = f"Adj Score vs {label_dict[column]} with {label_dict[size]} as Size<br><sup>X-Jittered for Visibility</sup>"
    else:
        title = f"Adj Score vs {label_dict[column]}<br><sup>X-Jittered for Visibility</sup>"

    data["jittered_col"] = data[column] + np.random.uniform(-jitter_strength, jitter_strength, size=len(data))
    
    fig = px.scatter(data_frame=data, x="jittered_col", y="adj_gross_score", color="name", color_discrete_map=color_map, size=size,
                     hover_name="name", labels={"adj_gross_score":"Adj. Score", "jittered_col":label_dict[column]}, 
                     title = title, hover_data={"name":False, "jittered_col":":.0f"})

    fig.update_layout(legend={"title":"Player Name"}, title={"y":.85})
    fig.update_traces(opacity=.6)
    
    return fig


def find_round(data:pd.DataFrame, name:str, date:pd.Timestamp='2024-07-22'):
    """
    Function to query a specific date for golf round data

    Args:
    ---------------
    data:pd.DataFrame | source of data
    names:str | player name to populate data for
    date:pd.Timestamp | date to search whether a round was played
    
    Returns:
    ---------------
    fig:plotly.graph_objects.Figure | barplot for each player from {names} who played a round of golf on {date}
    """
    label_dict = {
        "adj_gross_score":"Adjusted Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts",
        "3_putts": "3-Putts",
        "fairways_hit": "Fwys Hit",
        "gir": "G.I.R.",
        "penalty/ob": "Penalties/OB",
        "handicap":"Handicap Index",
        "birdies":"Birdies",
        "dbl_bogeys_plus":"Double or Worse",
        "profit/loss":"Profit/Loss",
        "match_format":"Match Format"
    }
    
    features = ["putts", "3_putts", "fairways_hit", "gir", "penalty/ob", "birdies", "dbl_bogeys_plus", "adj_gross_score", "profit/loss"]
    color_list = px.colors.qualitative.Bold

    fig = go.Figure()
    player_data = data_frame = data.loc[(data["date"] == date) & (data["name"] == name)]
    
    if not player_data.empty:
        
        # Create a bar for each feature
        for idx, feature in enumerate(features):
            fig.add_trace(go.Bar(
                x=[feature],
                y=player_data[feature].values,
                name=label_dict[feature],
                marker={"color":color_list[idx]}
            ))

        m_format = player_data["match_format"].iloc[0]
        
        fig.update_layout(
        title=f"Golf Round Data for {name} on {date.date()} <br><sup>- {str(m_format)}</sup>" if m_format != None else 
            f"Golf Round Data for {name} on {date.date()}<br><sup>(No format listed)</sup>",
        xaxis_title="Features",
        yaxis_title="Values",
        barmode='group',
        legend={"title":"Data Points:"},
        xaxis=dict(
                tickvals=features,
                ticktext=[label_dict[feature] for feature in features])
        )
    
        return fig


def total_profit(data:pd.DataFrame, color_map:dict={"Dave":'#636EFA', "Pete":'#EF553B', "Eric":'#00CC96'}):
    """
    Display the total +/- for a player's records in the data

    Args:
    ----------------
    data:pd.DataFrame | source of data
    color_map:dict | color mapping for consistency across plots

    Returns:
    fig.plotly.express.Figure | bar plot showing total profit/loss
    """
    
    fig = px.bar(data_frame = data.groupby("name")["profit/loss"].sum().reset_index(), x="name", y="profit/loss", color="name", 
                 color_discrete_map=color_map, title = "Total Profit/Loss for Each Player", hover_name="name", 
                 labels={"profit/loss":"Profit/Loss", "name":"Player Name"}, hover_data={"name":False})

    return fig


def profit_by_match_type(data:pd.DataFrame, aggfunc:str):
    """
    Display the PnL by match format

    Args:
    ---------------
    data:pd.DataFrame | source of data
    aggfunc:str | string, one of ["mean", "median", "sum"]

    Returns:
    ----------------
    fig:plotly.express.figure | bar plot showing PnL by category per player
    """

    label_dict = {
        "mean":"Average",
        "median":"50th Percentile",
        "sum":"Total"
    }
    
    fig = px.bar(data_frame = data.groupby(["name", "match_format"])["profit/loss"].agg([aggfunc]).reset_index(), x="name",
                y=aggfunc, color="match_format", barmode="group", hover_name = "name", hover_data={"name":False},
                labels={"match_format":"Match Format", "name":"Player Name", aggfunc:f"{label_dict[aggfunc]} Profit/Loss"},
                title = f"{label_dict[aggfunc]} Profit/Loss by Match Format")
    
    return fig


        
def explanation_of_plots():
    """
    Text explaining plotly functunality
    """

    import streamlit as st
    
    st.markdown("---")
    st.markdown(":blue[_A brief note about the plots:_]")
    st.markdown("You can isolate a plot component by double-clicking on it in the legend, or you can toggle on/off individual plot items by clicking on the desired item in the legend. You can also click and drag over quadrants of graphs to zoom in on areas of interest. Click the home icon in the upper-right corner or double-click on the plot to zoom back out to the original scope. Finally, as you move your mouse cursor over the plots, you will notice hover-values that display additional information. Thank you and enjoy the dashboard")
    st.markdown("---")