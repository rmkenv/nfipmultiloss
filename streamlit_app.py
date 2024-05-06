import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from st_paywall import add_auth

# Add authentication
add_auth(
    required=True,
    login_button_text="Subscriber Access",
    login_button_color="#FD504D",
    login_sidebar=True,
)

# Display subscription info
st.write("Congrats, you are subscribed!")
st.write("The email of the user is " + str(st.session_state.email))

# Function to extract payer emails from Buy Me a Coffee API response
def extract_payer_emails(json_response):
    payer_emails = []
    if "data" in json_response:
        for item in json_response["data"]:
            payer_email = item.get("payer_email")
            if payer_email:
                payer_emails.append(payer_email)
    return payer_emails

# Function to get active subscribers from Buy Me a Coffee
def get_bmac_payers():
    url = "https://buy-me-a-coffee-api-url"  # Replace with the actual Buy Me a Coffee API URL
    headers = {"Authorization": "Bearer your_api_key"}  # Replace with your API key
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return extract_payer_emails(response.json())  # Extract payer emails from JSON response
    else:
        raise Exception("Error fetching active subscriptions.")

# Set the page configuration
st.set_page_config(layout="wide")

# Title for the entire app
st.title("🎈 Integrated Streamlit App 🎈")

# Divider
st.markdown("---")

# Title for the NFIP data search functionality
st.subheader("Search NFIP Multiple Loss Properties")

# Data dictionary and options for dropdown
data_dictionary = {
    'psCountyCode': {'description': 'FIPS County Code', 'required': True, 'type': 'text'},
    'state': {'description': 'State', 'required': True, 'type': 'text'},
    # Add more items as needed
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
