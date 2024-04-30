import streamlit as st
from st_paywall import add_auth
import stripe
import os

# Setup Stripe
stripe.api_key = os.getenv('STRIPE_S_KEY')
stripe.default_http_client = stripe.http_client.RequestsClient()

def get_products():
    try:
        products = stripe.Product.list(limit=10)
        prices = stripe.Price.list(limit=10)
        products_with_prices = []

        for product in products.auto_paging_iter():
            product_prices = [
                price for price in prices.auto_paging_iter() if price.product == product.id
            ]
            products_with_prices.append({
                'product': product,
                'prices': product_prices
            })

        return products_with_prices
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        return []

def create_checkout_session(price_id):
    try:
        success_url = st.secrets["base_url"] + '/success?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = st.secrets["base_url"] + '/cancel'
        
        session = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1
                },
            ],
            mode="subscription",
            allow_promotion_codes=True,
        )
        return session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")

# Streamlit Page Configuration
st.set_page_config(layout="wide")
st.title("🎈 testing 🎈")
st.balloons()

# Authentication
add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=True,
)

st.write("Congrats, you are subscribed!")
st.write("The email of the user is " + str(st.session_state.email))

# Displaying products and initiating checkout
products_with_prices = get_products()
if products_with_prices:
    product_select = st.selectbox("Select a Product", options=[p['product']['name'] for p in products_with_prices], format_func=lambda x: x)
    selected_product = next((item for item in products_with_prices if item['product']['name'] == product_select), None)

    if selected_product:
        price_id = selected_product['prices'][0]['id']
        checkout_url = create_checkout_session(price_id)
        if checkout_url:
            st.markdown(f"[Subscribe]({checkout_url})", unsafe_allow_html=True)
