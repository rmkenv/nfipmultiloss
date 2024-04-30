import streamlit as st
from st_paywall import add_auth
import requests
import pandas as pd

# Streamlit Page Configuration
st.set_page_config(layout="wide")

# Authentication and Subscription Information
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()
add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=True,
)

# User-specific content after authentication
st.write("Congrats, you are subscribed!")
st.write("The email of the user is " + str(st.session_state.email))

# Define the data dictionary and options for dropdown
data_dictionary = {
    # Data dictionary contents here
    # Example:
    'zipCode': {'description': 'Zip Code', 'required': True, 'type': 'text'},
    'totalLosses': {'description': 'Total Losses', 'required': True, 'type': 'smallint'},
    'mostRecentDateofLoss': {'description': 'Most Recent Date of Loss', 'required': True, 'type': 'date'},
    # Add other fields as needed
}

# User input for data search
st.title("Search NFIP Multiple Loss Properties")
zip_code = st.text_input("Enter zip code:")
selected_columns = st.multiselect("Select columns to display:", options=[{'label': v['description'], 'value': k} for k, v in data_dictionary.items()])

# Search button action
search_button_clicked = st.button("Search")
if search_button_clicked:
    if zip_code and selected_columns:
        # Fetch data based on zip code and selected columns
        data = get_fema_data({'zipCode': zip_code})
        if data:
            # Filter data to show only selected columns
            table_data = [{col: record.get(col, '') for col in selected_columns} for record in data]
            st.write(pd.DataFrame(table_data))
        else:
            st.write("No results found for the specified zip code.")
    else:
        st.write("Please enter a zip code and select at least one column.")

# Function to fetch data from FEMA API
def get_fema_data(parameters={}):
    base_url = 'https://www.fema.gov/api/open/v1/NfipMultipleLossProperties'
    parameters['$allrecords'] = 'true'  # Retrieve all records
    try:
        response = requests.get(base_url, params=parameters)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json().get('NfipMultipleLossProperties', [])
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []
    except ValueError as e:
        st.error(f"Error parsing JSON response: {e}")
        return []
