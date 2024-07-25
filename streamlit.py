import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from utils import add_round, get_handicaps, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats, find_round, handicap_differentials

from streamlit_option_menu import option_menu

def main():

    # Config page layout
    st.set_page_config(page_title="Golf Group Handicap Tracker",
                   page_icon=':golf:',
                      layout="wide")
    
    # Page Title Text, Subtitle
    st.title(':orange[Golf Group Handicap Tracker]')
    st.subheader(":silver[_Statistics to Inform and Expedite Match Negotiations_]")
    st.markdown("---")

    # Body Paragraphs
    st.subheader(":blue[Project Background]")
    
    st.markdown("""Are your "friends" like mine, always negotiating in bad faith to get favorable lines on the 1st tee box? This project was born from that very frustration. The solution: verified player handicaps. There are barriers for the casual golfer to acquire a verified handicap.""")
    
    st.markdown("""The USGA (United States Golf Association) says that "...in order to establish and maintain a Handicap Index, a player must be a member of an authorized golf club." There are mobile applications that offer the ability to track golf statistics and calculate a handicap, but those apps often have associated subscription fees. Furthermore, if the members of my regular golf group don't want to use the app or pay the subscription, then their handicaps will continue to be unknown values.""")
    
    # Paragraph 2
    st.subheader(":blue[Calculating Player Handicaps]")
    st.markdown("""To calculate player handicaps, the "handicap differential" for _each round_ is recorded. The handicap differential is calculated:""")

    # Equation for Handicap Differential
    st.markdown(r"""
$$
\text{Handicap Differential} = \frac{(\text{Adjusted Gross Score} - \text{Course Rating}) \times 113}{\text{Slope Rating}}
$$
""")

    # Bullet Points for Components of the Equation
    st.markdown("""Where:
    
- Adjusted Gross Score (AGS): The score you actually shot, adjusted for equitable stroke control (ESC).
- Course Rating: A number representing the difficulty of a course for a scratch golfer.
- Slope Rating: A number representing the difficulty of a course for a bogey golfer compared to a scratch golfer. 
- The standard Slope Rating is 113.""")

    # Equitable Stroke Control Paragraph
    st.markdown("""_Equitable stroke control_ means that for a given handicap, there is a maximum allowable score on any individual hole. _"ESC"_ helps to protect a golfer's handicap from any individual hole where they play uncharacteristically bad golf. Those maximum scores for individual holes are capped as follows:""")
    
    # DF display
    st.dataframe(pd.read_csv("ESC.csv").rename(columns={"Course Handicap":"Player Handicap"}), use_container_width=True, hide_index=True)

    
    # Handicap Calc Paragraph
    st.markdown("""As you continue to record the handicap differentials for each round played, you will also need to meet a minimum threshold for rounds played. An official handicap can be obtained after recording 54 holes of golf. Your handicap will be calculated by averaging a certain number of your lowest scores depending on how many rounds you have recorded.""")

    # Df display
    st.dataframe(pd.read_csv("handicap_rds.csv", dtype={"Adjustment":str}).rename(columns={"Differentials to Use":"Differential Scores to Use",
                                                                "Adjustment":"Handicap Adjustment"}), use_container_width=True, hide_index=True)

    # Conclusion
    st.markdown("""Finally, you can find your handicap by applying this calculation:""")

    
    # Handicap Index Equation
    st.markdown(r"""
$$
\text{Handicap Index} = (\text{Average of Lowest Differentials} \times 0.96) + \text{Adjustment}
$$
""")

    
    # Synthetic Data Display
    st.markdown("---")

    st.subheader(":blue[While my friends and I collect some data...]")
    st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores. This data is purely for purposes of demonstration, and some of the statistics and relationships shown will likely not reflect reality for most golfers. \n \nThat being said, I am still the best golfer based on synthetic data......""")

    st.markdown(":blue[_A brief note about the plots:_]")
    st.markdown("You can isolate a plot component by double-clicking on it in the legend, or you can toggle on/off individual plot items by clicking on the desired item in the legend. You can also click and drag over quadrants of graphs to zoom in on areas of interest. Click the home icon in the upper-right corner or double-click on the plot to zoom back out to the original scope. Finally, as you move your mouse cursor over the plots, you will notice hover-values that display additional information. Thank you and enjoy the dashboard")
    
    st.markdown("---")

    
# --------------------------------------------------------------Visualizations------------------------------------------------------------
    
    # Tabs for data sources
    selected = option_menu(
        menu_title=None,
        options=['Fake Data', 'Real Data'],
        icons=['bar-chart-fill', 'person-fill'],  # 'bar-chart-fill', 'person-fill'
        orientation='horizontal',
    )

    # Change data source depending on tab selection
    if selected == "Fake Data":
        # Data load
        df = pd.read_csv("synthetic_data.csv", parse_dates=["date"]).sort_values(by="date")
    elif selected == "Real Data":
        st.subheader(":red[We are still collecting data currently, please bear with us.]")
        st.write('Switch back to the "Fake Data" tab to see all of the available visualizations')
        st.stop()
        
    # # Give the option to add data
    # st.subheader(":violet[Add your own data?:]")
    # col1, col2 = st.columns([1,1])
    # with col1:
    #     rd_name = st.text_input("Name:")
    #     rd_date = st.date_input("Date Played:")
    #     rd_adj_score = st.number_input("Adjusted Gross Score (Must know single hole limits)")
    #     rd_cr_rating = st.number_input("Course Rating:")
    #     rd_slope_rating = st.number_input("Slope Rating:")
    #     rd_putts = st.number_input("Number of Putts:", step=1)
    #     rd_three_putts = st.number_input("Number of 3-Putts:", step=1)
    # with col2:
    #     rd_fairways = st.number_input("Number of Fairways Hit:", step=1)
    #     rd_gir = st.number_input("Number of Greens in Regulation:", step=1)
    #     rd_penalty = st.number_input("Number of Penalty Shots:", step=1)
    #     rd_birdies = st.number_input("Number of Birdies:", step=1)
    #     rd_db_bogeys_plus = st.number_input("Number of Double-Bogeys or Worse:", step=1)
    #     profit_loss = st.number_input("Profit/Loss (in betting units)")

    # if st.button("Add Round?"):
    #     # Add the round to the df
    #     df.loc[len(df)] = add_round(name=rd_name, date=str(rd_date), adj_gross_score=rd_adj_score, course_rating=rd_cr_rating,
    #                                 slope_rating=rd_slope_rating, putts=rd_putts, three_putts=rd_three_putts,
    #                                 fairways=rd_fairways, gir=rd_gir, penalties=rd_penalty, birdies=rd_birdies,
    #                                 dbl_bogeys_plus=rd_db_bogeys_plus, profit_loss=profit_loss, calc_diff=True)
        
    #     # Update handicaps where applicable
    #     df = get_handicaps(df)
        
    #     st.write("Check out your new entry at the bottom of the dataframe")
    #     st.dataframe(df.drop(columns="jittered_col").tail(), hide_index=True, use_container_width=True)

    # def add_round(name:str, date:str, adj_gross_score:int, course_rating:np.number, slope_rating:np.number, \
    #           putts:int=np.nan, three_putts:int=np.nan, fairways:int=np.nan, gir:int=np.nan, penalties:int=np.nan, birdies:int=np.nan, dbl_bogeys_plus:int=np.nan, profit_loss:float=np.nan, calc_diff:bool=True) -> pd.Series:
    
    # Useful for labels, titles of plots
    label_dict = {
        "adj_gross_score":"Adjusted Gross Score", 
        "handicap_diff": "Handicap Differential",
        "putts": "Putts per Round",
        "3_putts": "3-Putts per Round",
        "fairways_hit": "Fairways Hit per Round",
        "gir": "Greens in Regulation",
        "penalty/ob": "Penalties / OB per Round",
        "handicap":"Handicap Index",
        # "birdies":"Birdies",
        # "dbl_bogeys_plus":"Double Bogey or Worse",
        # "profit/loss":"Profit/Loss"
    }
    
    # Also useful for labeling, titling, etc.
    reverse_labels = {val:key for key, val in label_dict.items()}
    
    # Numerical handicap displays for each player
    st.markdown("""<div style="text-align: center; font-size:40px; color:gold">
            <b><u><i>Current Player Handicaps:</i></u></b>
            </div>""", unsafe_allow_html=True)
    
    # finding unique players with valid handicaps
    names = df.dropna(subset="handicap")["name"].unique()
    cols = st.columns([1 for i in names])
    
    # Create a column for each player with their most up-to-date handicap
    for idx, name in enumerate(names):
        with cols[idx]:
            
            # Find the most recent value of "handicap" for the current name
            recent_handicap = df.loc[df['name'] == name, 'handicap'].iloc[-1]

            # Display that player's handicap
            st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="font-size:35px; color: orange;">{name}</h2>
            <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)
        

    # Trends, line plots
    st.markdown("---")
    st.subheader(":violet[Trends Over Time:]")
    st.write("Use the dropdown menu to select a metric and the date slider to select a range of dates")
    trend_var = st.selectbox("Trend Metric:", [*reverse_labels.keys()], index=7)
    trend_data = df.dropna(subset=reverse_labels[trend_var])

    # Set up min and max dates
    min_date = trend_data['date'].min().date()
    max_date = trend_data['date'].max().date()
    
    # Use st.date_input to select start and end dates
    start_date, end_date = st.slider("Date Range", min_value = min_date, max_value=max_date, \
                        value=(min_date, max_date), format="YYYY-MM-DD")
    
    # start_date = pd.to_datetime(st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date))
    # end_date = pd.to_datetime(st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date))
    
    # Line plot of all data with time slider to choose time window
    st.plotly_chart(plot_statistics(trend_data.loc[(trend_data["date"] >= pd.to_datetime(start_date)) & (trend_data["date"] <= pd.to_datetime(end_date))], reverse_labels[trend_var]))

    # Rolling averages to evaluate smoothed trends
    st.subheader(":violet[Rolling average statistics:]")
    st.write("Use the dropdown menu to select a metric and the slider to select the size of your window")
    roll_var = st.selectbox("Rolling Average Metric:", [*reverse_labels.keys()], index=0)
    window = st.slider("Number of Rounds to Include in the Rolling Window:", min_value=5, max_value = 30) 
    st.plotly_chart(rolling_avg(df, reverse_labels[roll_var], window))

    # Mean, median, stddev aggregate stats for different metrics
    st.subheader(":violet[Average, median, and standard deviation aggregate statistics:]")
    st.write("Use the dropdown menu to select a metric")
    agg_var = st.selectbox("Aggregate Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(mean_med_stats(df, reverse_labels[agg_var]))

    # Distribution plots for various metrics
    st.subheader(":violet[Distributions: Comparing distributions of different statistics across players:]")
    st.write("Use the dropdown menu to select a metric")
    hist_var = st.selectbox("Distribution Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(histplot(df, reverse_labels[hist_var]))

    # Proportion pie charts
    st.subheader(":violet[Proportions of contributing statistics:]")
    st.write("Use the dropdown menu to select a metric")

    pie_var = st.selectbox("Proportion Metric:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=1)
    cols = st.columns([1 for i in names])
    for idx, name in enumerate(names):
        with cols[idx]:
            st.plotly_chart(pie_chart(df, reverse_labels[pie_var], name))


    # Scatter plots of adj_gross_score vs other numeric variables with size option
    st.subheader(":violet[Adjusted Gross Score vs Contributing Statistics:]")
    st.write("Use the first dropdown menu to select a metric for the X-Axis and the second dropdown to optionally add a 'size' metric")
    
    scatter_var = st.selectbox("X-Variable:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    
    size_var = st.selectbox("Size-Variable (Optional):", [None] + [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    
    
    st.plotly_chart(scatter(data=df, column=reverse_labels[scatter_var], size=reverse_labels[size_var] if size_var else None)) 


    # Correlation analysis of the above scatterplot
    st.subheader(":violet[Feature Correlation:]")
    
    corr = df[["adj_gross_score", reverse_labels[scatter_var]]].corr().iloc[0,1]
    
    st.write(f'Overall Pearson Correlation for :blue[_Adjusted Gross Score and {scatter_var}_]: :green[**{corr:.3f}**]')

    # Boilerplate analysis options
    if abs(corr) <.4:
        # Weak correlation
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a weak correlation, and therefore it is likely that this statistic is not significantly influencing your scores.")
    
    # Positive correlation
    elif .7 > corr >= .4:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    elif corr > .7:
        
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong positive correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will also increase and vice versa.")
    
    # Negative correlation
    elif -.7 < corr <= -.4:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a moderate negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")
    elif corr < -.7:
        st.write(f"The relationship between Adjusted Gross Score and {scatter_var} demonstrates a strong negative correlation, meaning that as {scatter_var} increases, Adjusted Gross Score will decrease and vice versa.")

    # Player-by-player correlations
    st.write("Player by Player Correlation Breakdown for Comparison:")

    st.dataframe(df.groupby("name")[["adj_gross_score", reverse_labels[scatter_var]]].corr().reset_index()\
            .rename(columns={reverse_labels[scatter_var]:"Correlation", "name":"Player Name"})\
                 .loc[::2,["Player Name", "Correlation"]], hide_index=True)

    
    # Search for a specific date's records
    st.subheader(":violet[Search for a Specific Round:]")

    min_search_date = df['date'].min().date()
    max_search_date = df['date'].max().date()
    st.write("Use the first dropdown menu to select a date to search, then select an individual player for a graph of their data")
    round_date = st.date_input("Choose a Date to Search:", min_value=min_search_date, max_value=max_search_date, value=None)
    
    query_df = df.loc[df["date"] == pd.to_datetime(round_date)]
    if query_df.empty:
        st.subheader(":red[No records found for this date]")
    
    if not query_df.empty:         #### Edit Later #### 
        st.dataframe(query_df[["name"]+[key for key in label_dict.keys() if key not in ['birdies', 'dbl_bogeys_plus', 'profit/loss']]].rename(columns=label_dict).rename(columns={"name":"Player"})\
                     .drop(columns="Handicap Index"), hide_index=True, use_container_width=True)
        for name in query_df["name"].unique():
            st.plotly_chart(find_round(query_df, name, pd.to_datetime(round_date, format='YYYY-MM-dd')))
    
    
    # ------------------------------------- Sidebar - Bio info -------------------------------------------------
    st.sidebar.title('About Me:')
    
    # Variables for f-strings
    linkedin_url = "https://www.linkedin.com/in/david-hartsman-data/"
    github_url = "https://github.com/dvdhartsman"
    medium_url = "https://medium.com/@dvdhartsman"
    
    linkedin_markdown = f'[LinkedIn]({linkedin_url})'
    github_markdown = f'[GitHub]({github_url})'
    medium_markdown = f'[Blog]({medium_url})'
    
    # Text display
    st.sidebar.subheader('David Hartsman')
    st.sidebar.markdown(f"{linkedin_markdown} | {github_markdown} | {medium_markdown}", unsafe_allow_html=True)
    st.sidebar.write('dvdhartsman@gmail.com')
    



if __name__ == "__main__":
    main()