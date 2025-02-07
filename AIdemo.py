import streamlit as st
import google.generativeai as genai 

genai.configure(api_key='your-api-key-goes-here')

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('give me fun facts about pandas')

st.text(response.text)






#streamlit run AIdemo.py --server.enableCORS=false


if st.button("click me "):
    st.text("tag ur it")













# if st.button("Add Button"):
#     st.text("Boo!")
