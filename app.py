<<<<<<< HEAD
import streamlit as st
import pickle
import pandas as pd
import joblib

# โหลดโมเดล


model = joblib.load("sales_model.pkl")
encoder = joblib.load("encoder.pkl")

st.set_page_config(page_title="Retail Prediction", layout="centered")

st.title("🛒 Online Retail Prediction")
st.write("Predict total sales based on input data")

# input
quantity = st.number_input("Quantity", min_value=1, value=1)
price = st.number_input("Unit Price", min_value=0.0, value=1.0)
hour = st.slider("Hour", 0, 23, 12)
month = st.slider("Month", 1, 12, 6)

# dropdown ประเทศ
country = st.selectbox("Country", encoder.classes_)
country_encoded = encoder.transform([country])[0]

# predict
if st.button("Predict"):
    result = model.predict([[quantity, price, hour, month, country_encoded]])
    st.success(f"💰 Predicted Total Price: {result[0]:.2f}")

# เพิ่มกราฟเล็ก ๆ (ดูโปรขึ้น)
st.subheader("📊 Sample Data Preview")
df_sample = pd.DataFrame({
    "Feature": ["Quantity", "UnitPrice", "Hour", "Month"],
    "Value": [quantity, price, hour, month]
})
=======
import streamlit as st
import pickle
import pandas as pd
import joblib

# โหลดโมเดล


model = joblib.load("sales_model.pkl")
encoder = joblib.load("encoder.pkl")

st.set_page_config(page_title="Retail Prediction", layout="centered")

st.title("🛒 Online Retail Prediction")
st.write("Predict total sales based on input data")

# input
quantity = st.number_input("Quantity", min_value=1, value=1)
price = st.number_input("Unit Price", min_value=0.0, value=1.0)
hour = st.slider("Hour", 0, 23, 12)
month = st.slider("Month", 1, 12, 6)

# dropdown ประเทศ
country = st.selectbox("Country", encoder.classes_)
country_encoded = encoder.transform([country])[0]

# predict
if st.button("Predict"):
    result = model.predict([[quantity, price, hour, month, country_encoded]])
    st.success(f"💰 Predicted Total Price: {result[0]:.2f}")

# เพิ่มกราฟเล็ก ๆ (ดูโปรขึ้น)
st.subheader("📊 Sample Data Preview")
df_sample = pd.DataFrame({
    "Feature": ["Quantity", "UnitPrice", "Hour", "Month"],
    "Value": [quantity, price, hour, month]
})
>>>>>>> 9001a600f61977a563e2a61d6bd258657df5d223
st.bar_chart(df_sample.set_index("Feature"))