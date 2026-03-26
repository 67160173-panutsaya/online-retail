import streamlit as st
import pandas as pd
import joblib

# ตั้งค่าเว็บ
st.set_page_config(page_title="AI Retail Dashboard", layout="wide")

# โหลด model
@st.cache_resource
def load_model():
    model = joblib.load("sales_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

model, model_columns = load_model()

# Sidebar
st.sidebar.header("⚙️ Input")

quantity = st.sidebar.number_input("Quantity", 1, 1000, 10)
unit_price = st.sidebar.number_input("Unit Price", 0.01, 1000.0, 5.0)
hour = st.sidebar.slider("Hour", 0, 23, 12)
month = st.sidebar.slider("Month", 1, 12, 6)
day = st.sidebar.slider("Day", 1, 31, 15)
weekday = st.sidebar.slider("Weekday", 0, 6, 3)



# 🔥 สร้าง input
input_df = pd.DataFrame([{
    'Quantity': quantity,
    'UnitPrice': unit_price,
    'Hour': hour,
    'Month': month,
    'Day': day,
    'Weekday': weekday
}])

# 🔥 เพิ่ม column ประเทศทั้งหมดเป็น 0
for col in model_columns:
    if col.startswith("Country_"):
        input_df[col] = 0
# 🔥 One-hot
input_df = pd.get_dummies(input_df)

# ทำให้ column ตรงกับตอน train
input_df = input_df.reindex(columns=model_columns, fill_value=0)

# 💣 ลบ country ออกให้หมด
input_df = input_df[[col for col in input_df.columns if not col.startswith("Country_")]]

# 🔥 สร้าง input ให้ตรง model 100%
input_df = pd.DataFrame(columns=model_columns)

# ใส่ค่าเริ่มต้น = 0
input_df.loc[0] = 0

# ใส่ค่าที่ user เลือก
input_df.at[0, 'Quantity'] = quantity
input_df.at[0, 'UnitPrice'] = unit_price
input_df.at[0, 'Hour'] = hour
input_df.at[0, 'Month'] = month
input_df.at[0, 'Day'] = day
input_df.at[0, 'Weekday'] = weekday

# 🔥 ไม่ต้องมี Country แล้ว แต่ต้องกัน error
# ถ้ามี TotalSales โผล่มา → ลบทิ้ง
if 'TotalSales' in input_df.columns:
    input_df = input_df.drop(columns=['TotalSales'])

# 🔥 predict
prediction = model.predict(input_df)[0]

# ================= UI =================

st.title("📊 Smart Retail AI Dashboard")

st.write("ระบบนี้ใช้ Machine Learning ในการคาดการณ์ยอดขายจากข้อมูล เช่น จำนวนสินค้า ราคา และเวลา")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Sales", f"{prediction:,.2f}")
col2.metric("📦 Quantity", quantity)
col3.metric("💵 Price", unit_price)

st.write(f"📊 ยอดขายที่คาดการณ์: {prediction:,.2f}")

if prediction > 5000:
    st.success("🔥 ยอดขายสูงมาก (High Sales)")
elif prediction > 2000:
    st.warning("⚡ ยอดขายปานกลาง (Medium Sales)")
else:
    st.info("📉 ยอดขายค่อนข้างต่ำ (Low Sales)")

# กราฟ
chart_df = pd.DataFrame({
    'Feature': ['Quantity','UnitPrice','Hour','Month','Day','Weekday'],
    'Value': [quantity, unit_price, hour, month, day, weekday]
})

st.bar_chart(chart_df.set_index('Feature'))