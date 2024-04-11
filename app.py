import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Convert the data dictionary to a list of options for the dropdown
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

column_options = [{'label': v['description'], 'value': k} for k, v in data_dictionary.items()]

st.title("Search NFIP Multiple Loss Properties")

zip_code = st.text_input("Enter zip code:")
selected_columns = st.multiselect("Select columns to display:", options=column_options)

search_button_clicked = st.button("Search")

if search_button_clicked:
    if zip_code and selected_columns:
        params = {'zipCode': zip_code}
        data = get_fema_data(params)

        if data:
            table_data = [{col: record.get(col, '') for col in selected_columns} for record in data]
            st.write(pd.DataFrame(table_data))
        else:
            st.write("No results found for the specified zip code.")
    else:
        st.write("Please enter a zip code and select at least one column.")


def get_fema_data(parameters={}):
    base_url = 'https://www.fema.gov/api/open/v1/NfipMultipleLossProperties'
    parameters['$allrecords'] = 'true'
    try:
        response = requests.get(base_url, params=parameters)
        response.raise_for_status()
        data = response.json().get('NfipMultipleLossProperties', [])
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []
    except ValueError as e:
        st.error(f"Error parsing JSON response: {e}")
        return []
