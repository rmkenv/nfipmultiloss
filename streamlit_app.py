import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from st_paywall import add_auth
import stripe
from stripe import Customer  # Updated import

# Safe retrieval of Stripe API key from secrets
stripe_api_key = st.secrets["stripe"].get("secret_key_test", "default_test_key")
stripe.api_key = stripe_api_key

# Function to check payment status
def check_payment_status(user_email):
    # Retrieve customer based on email or other identifier
    customer = Customer.list(email=user_email)
    if customer.data:
        customer_details = customer.data[0]
        # Check subscriptions or payment intents as needed
        subscriptions = customer.Subscription.list(customer=customer_details.id)
        if subscriptions.data:
            for subscription in subscriptions.data:
                if subscription.status == "active":
                    return True
    return False

# Add authentication
add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=True,
)

# Safe retrieval of client_id from secrets
client_id = st.secrets.get("client_id", "default_client_id")

# Display subscription info and check for access
if check_payment_status(str(st.session_state.email)):
    st.write("Congrats, you are subscribed!")
    st.write("Access granted to premium features.")
else:
    st.error("You need a subscription to access this feature.")
    st.stop()

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
