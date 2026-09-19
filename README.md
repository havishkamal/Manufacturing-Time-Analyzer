# Manufacturing Time Analyzer — MVP

A first working Streamlit prototype for the student project.

### Features
- Upload CSV manufacturing data
- Total time, processing time and non-processing/review time KPIs
- Time by type
- Time by process
- Lost-time candidate reasons
- Raw data table
- CSV download

### Required CSV columns
`Process, Activity, Start Time, End Time, Duration (min), Time Type, Reason`

### Run
`pip install -r requirements.txt`
then
`streamlit run app.py`

This is an MVP. The classification is intentionally simple and must be validated/refined with real manufacturing data.
