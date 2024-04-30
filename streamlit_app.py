import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from st_paywall import add_auth

# Set the page configuration
st.set_page_config(layout="wide")

# Title for the entire app
st.title("🎈 Integrated Streamlit App 🎈")

# Subscription/authentication functionality
st.subheader("Tyler's Subscription App POC")
st.balloons()
add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=True,
)

st.write("Congrats, you are subscribed!")
user_email = str(st.session_state.get('email', 'No email provided'))
st.write(f"The email of the user is {user_email}")

# Divider
st.markdown("---")

# Title for the NFIP data search functionality
st.subheader("Search NFIP Multiple Loss Properties")

# Data dictionary and options for dropdown
data_dictionary = {
     'psCountyCode': {'description': 'FIPS County Code', 'required': True, 'type': 'text'},
    'state': {'description': 'State', 'required': True, 'type': 'text'},
    'stateAbbreviation': {'description': 'State Abbreviation', 'required': True, 'type': 'text'},
    'county': {'description': 'County', 'required': True, 'type': 'text'},
    'zipCode': {'description': 'Zip Code', 'required': True, 'type': 'text'},
    'reportedCity': {'description': 'Reported City', 'required': True, 'type': 'text'},
    'communityIdNumber': {'description': 'NFIP Community ID Number', 'required': True, 'type': 'text'},
    'communityName': {'description': 'NFIP Community Name', 'required': True, 'type': 'text'},
    'censusBlockGroup': {'description': 'Census Block Group FIPS', 'required': True, 'type': 'text'},
    'nfipRl': {'description': 'NFIP RL', 'required': True, 'type': 'boolean'},
    'nfipSrl': {'description': 'NFIP SRL', 'required': True, 'type': 'boolean'},
    'fmaRl': {'description': 'FMA RL', 'required': True, 'type': 'boolean'},
    'fmaSrl': {'description': 'FMA SRL', 'required': True, 'type': 'boolean'},
    'asOfDate': {'description': 'As of Date', 'required': True, 'type': 'date'},
    'floodZone': {'description': 'Flood Zone', 'required': True, 'type': 'text'},
    'latitude': {'description': 'Latitude', 'required': True, 'type': 'decimal'},
    'longitude': {'description': 'Longitude', 'required': True, 'type': 'decimal'},
    'occupancyType': {'description': 'Occupancy Type', 'required': True, 'type': 'smallint'},
    'originalConstructionDate': {'description': 'Original Construction Date', 'required': True, 'type': 'date'},
    'originalNBDate': {'description': 'Original NB Date', 'required': True, 'type': 'date'},
    'postFIRMConstructionIndicator': {'description': 'Post FIRM Construction Indicator', 'required': True, 'type': 'boolean'},
    'primaryResidenceIndicator': {'description': 'Primary Residence Indicator', 'required': True, 'type': 'boolean'},
    'mitigatedIndicator': {'description': 'Mitigated Indicator', 'required': True, 'type': 'boolean'},
    'insuredIndicator': {'description': 'Insured Indicator', 'required': True, 'type': 'boolean'},
    'totalLosses': {'description': 'Total Losses', 'required': True, 'type': 'smallint'},
    'mostRecentDateofLoss': {'description': 'Most Recent Date of Loss', 'required': True, 'type': 'date'},
    'id': {'description': 'ID', 'required': True, 'type': 'uuid'}
}

column_options = {k: v['description'] for k, v in data_dictionary.items()}

zip_code = st.text_input('Enter zip code')
selected_columns = st.multiselect('Select columns to display', options=list(column_options.keys()), format_func=lambda x: column_options[x])

if st.button('Search NFIP Data'):
    if zip_code and selected_columns:
        params = {'zipCode': zip_code, '$allrecords': 'true'}
        response = requests.get('https://www.fema.gov/api/open/v1/NfipMultipleLossProperties', params=params)
        if response.status_code == 200:
            data = response.json().get('NfipMultipleLossProperties', [])
            if data:
                table_data = pd.DataFrame(data)[selected_columns]
                st.dataframe(table_data)
                
                # Plotting if more than one column is selected for a better comparison
                if len(selected_columns) > 1:
                    fig = px.bar(table_data, x=selected_columns[0], y=selected_columns[1:])
                    st.plotly_chart(fig)
            else:
                st.error("No results found for the specified zip code.")
        else:
            st.error("Failed to fetch data from API.")
    else:
        st.warning("Please enter a zip code and select at least one column.")
