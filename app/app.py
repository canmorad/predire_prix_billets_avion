from html import escape
from pathlib import Path
from textwrap import dedent

import streamlit as st

from utils.constants import AIRLINES, CITIES, CLASSES, STOPS, TIMES, TIME_LABELS
from utils.model import predict_price

st.set_page_config(page_title='Flight Price Prediction', page_icon='✈️', layout='wide', initial_sidebar_state='collapsed')


def html_block(content):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


css = (Path(__file__).resolve().parent / 'styles' / 'style.css').read_text(encoding='utf-8')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">', unsafe_allow_html=True)

html_block('''
<div class="hero">
  <div class="hero-copy">
    <div class="eyebrow"><i class="fa-solid fa-plane-departure"></i> &nbsp; SMART TRAVEL · MACHINE LEARNING</div>
    <h1>Flight Price Prediction</h1>
    <p>Estimate your airfare in seconds with machine learning.</p>
  </div>
</div>
''')

html_block('<div class="section"><i class="fa-solid fa-route"></i> Your route</div>')
route_from, route_to, route_airline = st.columns(3, gap='medium')
with route_from:
    source_city = st.selectbox('From', CITIES, index=0)
with route_to:
    destination_city = st.selectbox('To', CITIES, index=1)
with route_airline:
    airline = st.selectbox('Airline', AIRLINES)

html_block('<div class="section"><i class="fa-solid fa-sliders"></i> Flight details</div>')
detail_class, detail_departure, detail_arrival = st.columns(3, gap='medium')
with detail_class:
    flight_class = st.selectbox('Travel class', CLASSES)
with detail_departure:
    departure_time = st.selectbox('Departure time', TIMES, format_func=lambda value: TIME_LABELS[value])
with detail_arrival:
    arrival_time = st.selectbox('Arrival time', TIMES, format_func=lambda value: TIME_LABELS[value])

detail_stops, detail_duration, detail_days = st.columns(3, gap='medium')
with detail_stops:
    stops = st.selectbox('Stops', list(STOPS), format_func=lambda value: STOPS[value])
with detail_duration:
    duration = st.number_input('Flight duration (hours)', min_value=0.1, max_value=50.0, value=2.5, step=0.1)
with detail_days:
    days_left = st.number_input('Days until departure', min_value=1, max_value=365, value=20, step=1)

html_block(f'<div class="route-summary"><i class="fa-solid fa-plane"></i><strong>{escape(source_city)}</strong><span>→</span><strong>{escape(destination_city)}</strong><span class="route-days">Departing in {days_left} days</span></div>')

if st.button('Estimate flight price', type='primary', use_container_width=True):
    if source_city == destination_city:
        st.warning('Departure and destination cities must be different.')
    else:
        features = {
            'airline': airline,
            'source_city': source_city,
            'departure_time': departure_time,
            'stops': stops,
            'arrival_time': arrival_time,
            'destination_city': destination_city,
            'class': flight_class,
            'duration': duration,
            'days_left': days_left,
        }
        try:
            with st.spinner('Calculating your estimate...'):
                prediction = predict_price(features)
            html_block(f'''<div class="result"><div class="tag"><i class="fa-solid fa-circle-check"></i> ESTIMATED TICKET PRICE</div><div class="price">₹ {prediction:,.0f}</div><div class="meta">{escape(airline)} &nbsp; · &nbsp; {escape(source_city)} → {escape(destination_city)} &nbsp; · &nbsp; {escape(flight_class)} &nbsp; · &nbsp; {escape(STOPS[stops])}</div><div class="note">Model estimate in Indian rupees (INR). Actual fares may vary.</div></div>''')
        except Exception as error:
            st.error(f'Prediction failed: {error}')

html_block('<div class="foot">Flight Price Prediction · Machine Learning Project</div>')
