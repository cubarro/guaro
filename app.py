# Del demo https://www.youtube.com/watch?v=VtrFjkSGgKM
# streamlit run demo4.py

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

st.write("## Uber en Nueva York")
st.markdown(
"""
Estás viendo un demo de app Streamlit que muestra sitios donde Uber ha recogido gente en Nueva York.
Se usa el deslizador (slider) para seleccionar la hora del día 
específica y *observe como cambia el mapa*.

[Código fuente de este documento](https://github.com/cubarro/guaro/blob/master/app.py)

[Aquí está el cófigo original](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)
""", unsafe_allow_html=True)

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

hora = st.sidebar.number_input('Hora',0,23,11)
data = data[data[DATE_TIME].dt.hour == hora]

' ## Mapa a las %s horas ' % hora
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

if st.checkbox('Mostrar los datos'):
	'Datos', data
