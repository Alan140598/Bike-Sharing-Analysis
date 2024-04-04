import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

#Set style seaborn
sns.set(style='whitegrid')
plt.style.use('dark_background')

# Mengimpor data yang sudah dibersihkan pada tahap data wrangling hingga visualisasi data 
day_df = pd.read_csv("https://raw.githubusercontent.com/Alan140598/Bike-Sharing-Dataset-Analysis/data/dashboard/day.csv")
day_df.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['holiday']
drop_col = ['weekday']
drop_col = ['temp']
drop_col = ['atemp']
drop_col = ['hum']
drop_col = ['windspeed']
for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Mengubah angka menjadi keterangan
day_df['mnth'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju/Hujan',
    4: 'Cuaca Buruk'
})

day_df['workingday'] = day_df['workingday'].map({
    0: 'Hari bukan kerja', 1: 'Hari kerja'
})
day_df['yr'] = day_df['yr'].map({
    0: '2011', 1: '2012'
})

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

#Menyiapkan monthly_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df


#Menyiapkan workingday_df
def create_workingday_df(df):
    workingday_df = df.groupby(by=["workingday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return workingday_df

#Menyiapkan weather_df
def create_weather_df(df):
    weather_df = df.groupby(by=["weathersit","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weather_df

# Memfilter data berdasarkan datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo pada dashboard yang akan dibuat
    st.image("https://raw.githubusercontent.com/Alan140598/Bike-Sharing-Dataset-Analysis/data/logo_bike_sharing.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                       (day_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
workingday_df = create_workingday_df(main_df)
weather_df = create_weather_df(main_df)

#Membuat judul pada dashboard
st.header('Bike Sharing Dashboard')

# Membuat jumlah penyewaan harian
st.subheader('Jumlah Sewa Harian')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Pengguna Kasual', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total Pengguna', value= daily_rent_total)

# Membuat jumlah penyewaan bulanan
st.subheader('Sewa Bulanan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['cnt'],
    marker='o', 
    linewidth=2,
    color='tab:cyan'
)

for index, row in enumerate(monthly_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10)

ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pengguna (Terdaftar dan Kasual)')
ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)
         
# Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca
st.subheader("Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots()
sns.barplot(data=weather_df, x="weathersit", y="cnt", hue="yr", palette="mako")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang Disewakan Berdasarkan Kondisi Cuaca")
plt.legend(title="Tahun", loc="upper right")  
for container in ax.containers:
    ax.bar_label(container, fontsize=8, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

# Jumlah Pengguna Sepeda Berdasarkan Hari Kerja
st.subheader("Jumlah Pengguna Sepeda Berdasarkan Hari Kerja")
fig, ax = plt.subplots()
sns.barplot(data=workingday_df, x="workingday", y="cnt", hue="yr", palette="magma")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang Disewakan Berdasarkan Hari Kerja")
plt.legend(title="Tahun", loc="upper left")  
for container in ax.containers:
    ax.bar_label(container, fontsize=8, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Alan Kurniawan February 2024')