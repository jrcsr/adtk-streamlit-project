# Anomaly Detection tool based on ADTK library (with Streamlit interface)

This repository is a small open-source project with the goal of experimenting on the ADTK library and the Streamlit framework
The ADTK methods settings may not be optimal for any relevant results, but this prject may evolve in the futur and I am open to any improvements !

- This tool currently implements only the PersistAD and LevelShiftAD method from the ADTK library, but it may include more in the future

## WebApp

This app is running and you can check the demo on the link below :


## Examples - Video

## Examples - Images

### 1 - Import some data

<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/step1.png" >

- Select the file you want to analyze

### 2 - Select your features and method of analysis

<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/step2.png" >

- Select in the right order the 2 columns required and the anomaly detection method

### 3 - Configure your model

<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/step3bis.png" >

- Enter your parameter for the analysis before clicking on the "Start Analysis" button

### 4 - Results and data exportation

<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/results1.png" >
<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/results2.png" >

- Visualize the results in a graphic fromat as well as in a table format

<img src="https://github.com/jrcsr/adtk-streamlit-project/blob/main/assets/download.png" >

- Click on the Download button to get the .csv file of the detected anomalies from your uploaded file


## Requirements

Python 3.7+
ADTK
Streamlit
Pandas

```bash
pip install adtk streamlit plotly pandas
```

## Installation

- Clone the repository: `git clone <https://github.com/jrcsr/adtk-streamlit-project>`
- Change to the repository directory: `cd adtk-streamlit-project`

## Usage

- Run the app with the following command: `streamlit run app.py`
- The app should open in a new browser window.
