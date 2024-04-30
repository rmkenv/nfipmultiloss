import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import stripe

# Set the page configuration
st.set_page_config(layout="wide")

# Title for the entire app
st.title("🎈 Integrated Streamlit App 🎈")

# Initialize Stripe
stripe.api_key = "stripe_api_key"  # Replace with your Stripe API key

# Stripe OAuth URL
stripe_oauth_url = "stripe_link"

# Button to initiate Stripe authentication
if st.button("Login with Stripe"):
    st.markdown(f"[Click here to login with Stripe]({stripe_oauth_url})")

# Handle Stripe callback
if st.url_contains("/stripe_callback"):
    # Extract authorization code from URL
    authorization_code = st.url_query_params["code"]

    # Exchange authorization code for access token
    response = stripe.OAuth.token(grant_type="authorization_code", code=authorization_code)

    # Use access token to fetch user information
    access_token = response["access_token"]
    user_info = stripe.Account.retrieve(access_token)

    # Display user information
    st.write("Logged in user:")
    st.write(user_info)

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



# Handle Stripe callback
current_url = st.url
if "/stripe_callback" in current_url:
    # Extract authorization code from URL
    authorization_code = st.url_query_params["code"]

