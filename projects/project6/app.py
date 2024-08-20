import pandas as pd
import numpy as np
import pickle
import streamlit as st
model=pickle.load(open('model.pk1','rb'))
df=pd.read_csv("final_data.csv")
st.header("Car price prediction")
l=df['Manufacturer'].unique()
v=dict()
l2=[]

brand=st.selectbox("Chose car brand",df["Manufacturer"].unique())
c_model=st.selectbox("Chose car model",list(df[df["Manufacturer"] == brand]["Model_name"].unique()))
location=st.selectbox("Chose your location",df["Location"].unique())
year=st.number_input("Enter the year of car",min_value=1900,max_value=2023)
mileage=st.number_input("Enter the mileage of car",min_value=0,max_value=999999)
dealer=st.selectbox("car from dealer ?",["yes","no"])
dealer=int(dealer=="yes")
def gen_l(v):
    return [i for i in range(len(v))]
if st.button("Estimate value"):
    input_data_model = pd.DataFrame(
    [[location,mileage,year,dealer,brand,c_model]],
    columns=['Location','Miles','Year','Dealership','Manufacturer','Model_name'])
    input_data_model["Location"].replace(df["Location"].unique(),gen_l(df["Location"].unique()),inplace=True)
    input_data_model["Manufacturer"].replace(df["Manufacturer"].unique(),gen_l(df["Manufacturer"].unique()),inplace=True)
    input_data_model["Model_name"].replace(df["Model_name"].unique(),gen_l(df["Model_name"].unique()),inplace=True)
    price=model.predict(input_data_model)
    st.markdown("estimated car price is : $"+str(price[0].round(4)))