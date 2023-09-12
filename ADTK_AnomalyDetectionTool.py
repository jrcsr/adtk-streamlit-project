import pandas as pd
import streamlit as st
from adtk.data import validate_series
from adtk.detector import *
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_icon="📈")

if "stage" not in st.session_state:
    st.session_state.stage = 0


def set_state(i):
    st.session_state.stage = i


col1_, col2_, col3_ = st.columns([1, 3, 1])

with col2_:
    st.write("## Anomaly Detection Tool (ADTK library)")
    st.write("PersistAD model from ADTK Anomaly Detection Python library")

    uploaded_file = st.file_uploader("Choose your CSV file", type=["csv"])


## Convert uploaded file to the preferred format of only 2 columns with dates and numerical values informations
def transform_(uploaded_file, date, value):
    s = uploaded_file[[date, value]]
    s[date] = pd.to_datetime(s[date])
    s = s.set_index(date)
    s = s[value]
    s = validate_series(s)
    return s


## Create and display the resulting analyzed data into a time-series plot and a data table
def format_and_display(data, anomalies, value):
    tab1, tab2 = st.tabs(["Anomaly graph", "Anomaly table"])
    with tab1:  # Graph
        fig = px.scatter(data, color=anomalies["anomaly"])
        st.plotly_chart(fig, use_container_width=True)
    with tab2:  # Table
        vals = anomalies["anomaly"]
        fill_color = [
            "rgb(0,0,0)",
            ["rgb(230,0,0)" if v == True else "rgb(0,0,0)" for v in vals],
        ]
        table_d = anomalies.merge(data, on="date", how="left")
        fig1 = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["date"] + list(table_d.columns),
                        align="left",
                        font=dict(
                            size=14,
                        ),
                    ),
                    cells=dict(
                        values=[table_d.index, table_d["anomaly"], table_d[value]],
                        align="left",
                        fill=dict(color=fill_color),
                        font=dict(
                            size=14,
                        ),
                    ),
                )
            ]
        )
        st.plotly_chart(fig1, use_container_width=True)


if uploaded_file is not None:
    with col2_:
        file = pd.read_csv(uploaded_file)
        st.table(file.head(10))

        st.markdown("***")
        st.markdown(
            """
        ##### Your file need to have only two columns :
        - a date format one (for the x-axis)
        - one with numerical values (for the y-axis)
        """
        )

        options_ = list(
            st.multiselect(
                "Please select your two features from your imported file - in the correct order",
                list(file.columns),
                list(file.columns)[0:2],
            )
        )

        selection = st.selectbox(
            "Choose your anomaly detection method from the drop-down list below :",
            ("", "PersistAD", "LevelShiftAD"),
        )

        if selection != "":
            if selection == "PersistAD":
                st.write(
                    "PersistAD compares each time series value with its previous values"
                )
            if selection == "LevelShiftAD":
                st.write(
                    "LevelShiftAD detects shift of value level by tracking the difference between median values at two sliding time windows next to each other. It is not sensitive to instantaneous spikes and could be a good choice if noisy outliers happen frequently"
                )

            st.button(
                "Select your features and method",
                use_container_width=True,
                on_click=set_state,
                args=[1],
            )
            if st.session_state.stage >= 1:
                data = transform_(file, options_[0], options_[1])

                if selection == "PersistAD":
                    st.write("##### Your ADTK PersistAD model parameters :")
                    col1, col2 = st.columns(2)
                    with col1:
                        c_param = st.text_input(
                            "Input your c parameter value for the model to train to"
                        )
                    with col2:
                        window_param = st.text_input(
                            "Input your window width for your model to train to"
                        )
                    option = st.selectbox(
                        "Choose to detect positive change or negative change of data flow",
                        ("", "positive", "negative"),
                    )
                    if option != "":
                        st.button(
                            "Start Analysis",
                            use_container_width=True,
                            on_click=set_state,
                            args=[2],
                        )
                        if st.session_state.stage >= 2:
                            persist_ad = PersistAD(
                                c=float(c_param), side=option, window=int(window_param)
                            )
                            anomalies = persist_ad.fit_detect(data)
                            anomalies = anomalies.to_frame()
                            anomalies = anomalies.rename(
                                columns={options_[1]: "anomaly"}
                            )
                            format_and_display(
                                data=data, anomalies=anomalies, value=options_[1]
                            )
                            st.download_button(
                                "Download the Anomaly table to .csv file",
                                use_container_width=True,
                                data=anomalies.to_csv().encode("utf-8"),
                                file_name=uploaded_file.name[:-4] + "_anomalies.csv",
                                mime="text/csv",
                            )

                elif selection == "LevelShiftAD":
                    st.write("##### Your ADTK LevelShiftAD model parameters :")
                    col1, col2 = st.columns(2)
                    with col1:
                        c_param = st.text_input(
                            "Input your c parameter value for the model to train to"
                        )
                    with col2:
                        window_param = st.text_input(
                            "Input your window width for your model to train to"
                        )
                    option = st.selectbox(
                        "Choose to detect positive change or negative change of data flow",
                        ("", "positive", "negative"),
                    )
                    if option != "":
                        st.button(
                            "Start Analysis",
                            use_container_width=True,
                            on_click=set_state,
                            args=[2],
                        )
                        if st.session_state.stage >= 2:
                            level_shift_ad = LevelShiftAD(
                                c=float(c_param), side=option, window=int(window_param)
                            )
                            anomalies = level_shift_ad.fit_detect(data)
                            anomalies = anomalies.to_frame()
                            anomalies = anomalies.rename(
                                columns={options_[1]: "anomaly"}
                            )
                            format_and_display(
                                data=data, anomalies=anomalies, value=options_[1]
                            )
                            st.download_button(
                                "Download the Anomaly table to .csv file",
                                use_container_width=True,
                                data=anomalies.to_csv().encode("utf-8"),
                                file_name=uploaded_file.name[:-4] + "_anomalies.csv",
                                mime="text/csv",
                            )
        else:
            st.write("Please select a method")
