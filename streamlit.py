import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st


from utils import add_round, get_handicap, fill_handicaps, plot_statistics, histplot, pie_chart, dist_plot, rolling_avg, scatter, mean_med_stats

def main():

    st.set_page_config(page_title="Golf Group Handicap Tracker",
                   page_icon=':golf:',
                      layout="wide")
    
    st.title(':orange[Golf Group Handicap Tracker]')
    st.subheader(":silver[_Statistics to Inform and Expedite Match Negotiations_]")
    st.markdown("---")

    st.subheader(":blue[Project Background]")
    st.markdown("""Are your "friends" like mine, always negotiating in bad faith to get favorable lines on the 1st tee box? This project was born from that very frustration. The solution: verified player handicaps. There are barriers for the casual golfer to acquire a verified handicap.""")
    st.markdown("""The USGA (United States Golf Association) says that "...in order to establish and maintain a Handicap Index, a player must be a member of an authorized golf club." There are mobile applications that offer the ability to track golf statistics and calculate a handicap, but those apps often have associated subscription fees. Furthermore, if the members of my regular golf group don't want to use the app or pay the subscription, then their handicaps will continue to be unknown values.""")
    
    st.subheader(":blue[Calculating Player Handicaps]")
    st.markdown("""To calculate player handicaps, the "handicap differential" for _each round_ is recorded. The handicap differential is calculated:""")

    st.markdown(r"""
$$
\text{Handicap Differential} = \frac{(\text{Adjusted Gross Score} - \text{Course Rating}) \times 113}{\text{Slope Rating}}
$$
""")

    st.markdown("""Where:
    
- Adjusted Gross Score (AGS): The score you actually shot, adjusted for equitable stroke control (ESC).
- Course Rating: A number representing the difficulty of a course for a scratch golfer.
- Slope Rating: A number representing the difficulty of a course for a bogey golfer compared to a scratch golfer. 
- The standard Slope Rating is 113.""")

    st.markdown("""_Equitable stroke control_ means that for a given handicap, there is a maximum allowable score on any individual hole. _"ESC"_ helps to protect a golfer's handicap from any individual hole where they play uncharacteristically bad golf. Those maximum scores for individual holes are capped as follows:""")
    st.dataframe(pd.read_csv("ESC.csv").rename(columns={"Course Handicap":"Player Handicap"}), use_container_width=True, hide_index=True)

    st.markdown("""As you continue to record the handicap differentials for each round played, you will also need to meet a minimum threshold for rounds played. An official handicap can be obtained after recording 54 holes of golf. Your handicap will be calculated by averaging a certain number of your lowest scores depending on how many rounds you have recorded.""")

    st.dataframe(pd.read_csv("handicap_rds.csv").rename(columns={"Differentials to Use":"Differential Scores to Use",
                                                                "Adjustment":"Handicap Adjustment"}), use_container_width=True, hide_index=True)

    st.markdown("""Finally, you can find your handicap by applying this calculation:""")

    st.markdown(r"""
$$
\text{Handicap Index} = (\text{Average of Lowest Differentials} \times 0.96) + \text{Adjustment}
$$
""")

    st.markdown("---")

    st.subheader(":blue[While my friends and I collect some data...]")
    st.markdown("""I have generated some synthetic data to demonstrate the visualizations we will use to track and analyze our scores:""")
    
    # Data load
    df = pd.read_csv("synthetic_data.csv", parse_dates=["date"]).sort_values(by="date")

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

    reverse_labels = {val:key for key, val in label_dict.items()}
    
    st.markdown("""<div style="text-align: center; font-size:40px; color:gold">
            <b><u><i>Current Player Handicaps:</i></u></b>
            </div>""", unsafe_allow_html=True)
    names = df["name"].unique()
    cols = st.columns([1 for i in names])
    
    for idx, name in enumerate(names):
        with cols[idx]:
            # Find the most recent value of "twentyRd_handicap" for the current name
            recent_handicap = df.loc[df['name'] == name, 'twentyRd_handicap'].iloc[-1]
            # st.metric(label=f"{name}", value=recent_handicap.round(3))
            st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="font-size:35px; color: orange;">{name}</h2>
            <h2 style="font-size:30px; color: #40a3ff;">{recent_handicap:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)
        

    st.markdown("---")
    st.subheader(":violet[Trends Over Time:]")
    trend_var = st.selectbox("Trend Metric:", [*reverse_labels.keys()], index=0)
    trend_data = df.dropna(subset=reverse_labels[trend_var])

    # Set up min and max dates
    min_date = trend_data['date'].min().date()
    max_date = trend_data['date'].max().date()
    
    # Use st.date_input to select start and end dates
    start_date, end_date = st.slider("Date Range", min_value = min_date, max_value=max_date, \
                        value=(min_date, max_date), format="YYYY-MM-DD")
    
    # start_date = pd.to_datetime(st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date))
    # end_date = pd.to_datetime(st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date))
    
    st.plotly_chart(plot_statistics(trend_data.loc[(trend_data["date"] >= pd.to_datetime(start_date)) & (trend_data["date"] <= pd.to_datetime(end_date))], "twentyRd_handicap"))

    st.subheader(":violet[Distributions: Comparing distributions of different statistics across players:]")
    hist_var = st.selectbox("Distribution Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(histplot(df, reverse_labels[hist_var]))

    st.subheader(":violet[Proportions of contributing statistics:]")

    pie_var = st.selectbox("Proportion Metric:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    cols = st.columns([1 for i in names])
    for idx, name in enumerate(names):
        with cols[idx]:
            st.plotly_chart(pie_chart(df, reverse_labels[pie_var], name))

    
    st.subheader(":violet[Average, median, and standard deviation aggregate statistics:]")
    agg_var = st.selectbox("Aggregate Metric:", [*reverse_labels.keys()], index=0)
    st.plotly_chart(mean_med_stats(df, reverse_labels[agg_var]))

    
    st.subheader(":violet[Rolling average statistics:]")
    roll_var = st.selectbox("Rolling Average Metric:", [*reverse_labels.keys()], index=0)
    window = st.slider("Number of Rounds to Include in the Rolling Window:", min_value=5, max_value = 30) 
    st.plotly_chart(rolling_avg(df, reverse_labels[roll_var], window))


    st.subheader(":violet[Adjusted Gross Score vs Contributing Statistics:]")
    scatter_var = st.selectbox("X-Variable:", [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Five-Round Rolling Handicap", 
                                                   "Ten-Round Rolling Handicap", "Twenty-Round Rolling Handicap"]], index=0)
    size_var = st.selectbox("Size-Variable (Optional):", [None] + [key for key in reverse_labels.keys() if key not in \
                                                  ["Adjusted Gross Score", "Handicap Differential", "Handicap Index"]], index=0)
    
    
    st.plotly_chart(scatter(data=df, column=reverse_labels[scatter_var], size=reverse_labels[size_var] if size_var else None)) 



if __name__ == "__main__":
    main()