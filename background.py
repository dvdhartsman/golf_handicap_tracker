import pandas as pd
import numpy as np
import streamlit as st

def background_info():
    """
    Displays the text and background information for this project
    """

    
    # Body Paragraphs
    st.subheader(":blue[Project Background]")
    
    st.markdown("""Are your "friends" like mine, always negotiating in bad faith to get favorable lines on the 1st tee box? This project was born from that very frustration. The solution: verified player handicaps. There are barriers for the casual golfer to acquire a verified handicap.""")
    
    st.markdown("""The USGA (United States Golf Association) says that "...in order to establish and maintain a Handicap Index, a player must be a member of an authorized golf club." There are mobile applications that offer the ability to track golf statistics and calculate a handicap, but those apps often have associated subscription fees. Furthermore, if the members of my regular golf group don't want to use the app or pay the subscription, then their handicaps will continue to be unknown values.""")
    
    # Paragraph 2
    st.subheader(":blue[Calculating Player Handicaps]")
    st.markdown("""To calculate player handicaps, the :green[_"handicap differential"_] for _each individual round_ must first be recorded. The handicap differential is calculated:""")

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
    st.markdown(""":green[_Equitable stroke control_] means that for a given handicap, there is a maximum allowable score on any individual hole. :green[_"ESC"_] helps to protect a golfer's handicap from the negative impact of any individual hole where they play uncharacteristically bad golf. Those maximum scores for individual holes are capped as follows:""")
    
    # DF display
    st.dataframe(pd.read_csv("ESC.csv").rename(columns={"Course Handicap":"Player Handicap"}), use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # Handicap Calc Paragraph
    st.markdown("""As you continue to record the handicap differentials for each round of golf you have played, you will also need to meet a minimum threshold of total rounds played. An official handicap can be obtained after recording 54 holes of golf (three 18-hole rounds). Your handicap will be calculated by averaging a specific number of your lowest scores over a specified window of your most recent scores depending on how many rounds you have recorded.""")

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

    st.markdown("""Now that you understand the process of getting a handicap index, please feel free to investigate the synthetic data and visualizations I have loaded to see how our incoming data will be stored and analyzed. My personal golf data will be trickling in slowly as well, so stay tuned to either laugh at me or be impressed!""")

    
    # Synthetic Data Display
    st.markdown("---")