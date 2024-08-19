import pandas as pd
import numpy as np
import pickle
import streamlit as st
model=pickle.load(open('model.pk1','rb'))
st.header("Car price prediction")