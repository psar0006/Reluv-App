from pycaret.regression import load_model, predict_model
import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image

im = Image.open('Reluv_icon.png')
st.set_page_config(page_title="Reluv Price Estimator", page_icon=im, initial_sidebar_state="auto", menu_items={'About': 'https://reluv.com.au/elements/pages/about/'          
    })

def payout_percentage(x):
  if x <= 20:
    return x
  elif x > 20 and x <= 50:
    return round(float((x/(0.95+(0.024*(x-20))))),1)
  elif x > 50 and x <= 80:
    return round(float((x/(1.61+(0.013*(x-50))))),1)
  elif x > 80 and x <= 100:
    return round(float((x/(1.95+(0.0025*(x-100))))),1)
  else:
    return 60  


database = pd.read_csv('sample_data.csv')
model = load_model('Retrain_Model_Pipeline')
d = {'Reluv Listed Price': ['$0.00-$20.00', '$20.01-$50.00', '$50.01-$80.00', '$80.01-$100', '$100+'], 'Payout': ['5-20%', '21-30%', '31-40%', '41-50%', '60%']}
table = pd.DataFrame(data=d)

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions
image = Image.open('output-onlinepngtools.png')
url = "https://reluv.com.au/learn-more/brands-we-do-not-accept/"
about_url = "https://reluv.com.au/elements/pages/about/"
sustainability_url = "https://reluv.com.au/sustainability/"
social_url = "https://reluv.com.au/our-impact/"
faq_url = "https://reluv.com.au/elements/pages/faq/"
return_policy_url = "https://reluv.com.au/return-policy/"
private_policy_url = "https://reluv.com.au/privacy-policy-2/"
blog_url = "https://reluv.com.au/?page_id=79"
zip_url = "https://reluv.com.au/zip-own-it-now-pay-later/"
contact_url = "https://reluv.com.au/elements/pages/contact/"

st.image(image, use_column_width =False)
st.header("Reluv Payout Estimator: ")
st.markdown("Type in or select from dropdowns and click the estimate button")
st.markdown("Note: There are a number of brands we cannot resell. Please check out the list of brands we currently do not accept [here](%s)" % url)
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#FFC0CB,#FFC0CB);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)
st.sidebar.image(image, use_column_width =False)
st.sidebar.markdown("[About Us](%s)" % about_url)
st.sidebar.markdown("[Sustainability](%s)" % sustainability_url)
st.sidebar.markdown("[Social Impact](%s)" % social_url)
st.sidebar.markdown("[FAQ](%s)" % faq_url)
st.sidebar.markdown("[Return Policy](%s)" % return_policy_url)
st.sidebar.markdown("[Private Policy](%s)" % private_policy_url)
st.sidebar.markdown("[Blog](%s)" % blog_url)
st.sidebar.markdown("[ZIP- Own Pay It Now Pay Later](%s)" % zip_url)
st.sidebar.markdown("[Contact Us](%s)" % contact_url)
#Now we will take user input one by one as per our dataframe
#Brand
Brand = st.selectbox('Brand', database['Brand'].sort_values().unique())
#Type of clothing
Category = st.selectbox("Category", database['Category'].sort_values().unique())
#Condtition
condition = st.selectbox("Condition", database['Condition'].sort_values().unique())
#Occasion
occasion = st.selectbox("Occasion", database['Occasion'].sort_values().unique())
#Prediction
st.markdown("Disclaimer: The amount displayed is an estimate only. Please be aware that the item will be priced after physical inspection and at Reluv's discretion.")
user_inputs = {'Brand': Brand, 'Category': Category,
            'Condition': condition, 'Occasion': occasion
            }
user_inputs_df = pd.DataFrame([user_inputs])

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table
st.table(table)


if st.button('Estimate Price'):
  prediction = predict(model, user_inputs_df)
  true_val = np.square(prediction)
  lower_val = round(true_val - 2.5)
  upper_val = round(true_val + 2.5)
  payout_per = payout_percentage(true_val)
  upper_payout_val = str(round(float(((payout_per/100)*upper_val)),2))
  lower_payout_val = str(round(float(((payout_per/100)*lower_val)),2))
  money = str(true_val)
  upper_money = str(upper_val)
  lower_money = str(lower_val)
  st.subheader("Estimated Price Range: " + "\$"+ lower_money + " - " + "\$"+ upper_money)
  st.subheader("Approximate payout: " + "\$" +lower_payout_val + ' - '+ "\$" + upper_payout_val)
