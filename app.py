
#IMPORTS

import streamlit as st
import pandas as pd
import numpy as np
import operator
import requests
from streamlit_lottie import st_lottie

# 1 - HEADER
# Application title & subtitle
'''
# B I R D S
'''

# Quick instructions for the user
st.header('Welcome to our birds identification project!')
instructions = """
    Either upload your own record or select from the sidebar to get a prerecorded file.
     
    The file you select or upload will be sent through the Deep Neural Network in real-time 
    and the output will be displayed to the screen.
    """
st.write(instructions)

# File uploader
file = st.file_uploader('Upload a record')
if file is not None:
    st.audio(file, format='audio/ogg')
    bytesdata = file.read()
    with open("pip.ogg", "wb") as file:
        file.write(bytesdata)

# API call

button = st.button('Identify this Bird !','Submit','Clic to identify this record')
if button:
    prediction = {}
    url = "https://birdsapi-kkxhmnngqq-ew.a.run.app/uploadfile/"
    files = {"file": bytesdata}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        resp = response.json()
        prediction = resp
        st.subheader("🦅🐤 Hurray ! Looks like we found something ! 🐦🦜")
        #prediction = {'Acrocephalus palustris': 3.1710833e-08, 'Sylvia atricapilla': 2.5642566e-07, 'Hirundo rustica': 0.99999976}
        top_prediction = max(prediction.items(), key=operator.itemgetter(1))[0]
        top_prediction_rate = max(prediction.items(), key=operator.itemgetter(1))[1]


        # ---------------WIKIPEDIA API-----------------
        url = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{top_prediction}'
        response_wiki = requests.get(url)
        if response_wiki.status_code == 200:
            common_name = response_wiki.json()['title']
            image_url = response_wiki.json()['thumbnail']['source']
            #print(common_name)
        else:
            "😬🤖 API error 🤖😬"
            response_wiki
        # ---------------/WIKIPEDIA API-----------------


        st.subheader("Here is the most likely bird : ")
        st.image(image_url)
        st.title(common_name)
        st.write(top_prediction)

        st.subheader("With a confidence level of : " + str(round(top_prediction_rate, 2)))



        st.subheader("Here are the three most likely bird species")
        df = pd.DataFrame(data=np.zeros((3, 2)), 
                            columns=['Species', 'Confidence Level'])


        df = pd.DataFrame(columns=['Species', 'Confidence Level'])
        for name, prob in prediction.items():
            link = 'https://fr.wikipedia.org/wiki/' + name.lower().replace(' ', '_')
            df.loc[name, 'Species'] = f'<a href="{link}" target="_blank">{name.title()}</a>'
            df.loc[name, 'Confidence Level'] = prob
            
        df.sort_values(by='Confidence Level', ascending=False, inplace=True)
        df.reset_index(inplace=True)

        st.write(df.to_html(escape=False), unsafe_allow_html=True)

        col1, col2, col3 = st.beta_columns(3)
        #prediction1, prediction2, prediction3 = df.iloc[0, 'Species'], df.iloc[1, 'Species'], df.iloc[2, 'Species'],
        prediction1 = sorted(prediction, key=prediction.get,reverse=True)[0]
        prediction2= sorted(prediction, key=prediction.get,reverse=True)[1]
        prediction3 = sorted(prediction, key=prediction.get,reverse=True)[2]
        
        url1 = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{prediction1}'
        response_wiki1 = requests.get(url1)
        if response_wiki1.status_code == 200:
            common_name1 = response_wiki1.json()['title']
            image_url1 = response_wiki1.json()['thumbnail']['source']
            
        col1.header(common_name1)
        col1.image(image_url1, use_column_width=True)

        url2 = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{prediction2}'
        response_wiki2 = requests.get(url2)
        if response_wiki2.status_code == 200:
            common_name2 = response_wiki2.json()['title']
            image_url2 = response_wiki2.json()['thumbnail']['source']
            
        col2.header(common_name2)
        col2.image(image_url2, use_column_width=True)

        url3 = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{prediction3}'
        response_wiki3 = requests.get(url3)
        if response_wiki3.status_code == 200:
            common_name3 = response_wiki3.json()['title']
            image_url3 = response_wiki3.json()['thumbnail']['source']
            
        col3.header(common_name3)
        col3.image(image_url3, use_column_width=True)

    else:
        "😬🤖 API error 🤖😬"
        response
        
        
# Animation from Lottie    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets4.lottiefiles.com/private_files/lf30_4r6a1nau.json"
#lottie_url = "https://assets2.lottiefiles.com/private_files/lf30_lmsysoyy.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json)



#--------------------------- SIDE BAR --------------------------


# for name, prob in prediction.items():
#             url1 = 'https://fr.wikipedia.org/wiki/' + name.lower().replace(' ', '_')
#             df.loc[name, 'Species'] = f'<a href="{link}" target="_blank">{name.title()}</a>'
#             df.loc[name, 'Confidence Level'] = prob
            
# url = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{top_prediction}'
# response_wiki = requests.get(url)
# if response_wiki.status_code == 200:
#     common_name = response_wiki.json()['title']
#     image_url = response_wiki.json()['thumbnail']['source']
#     #print(common_name)
# else:
#     "😬🤖 API error 🤖😬"
#     response_wiki


logo = st.sidebar.image('./images/logo_100px.png')

birds = st.sidebar.subheader("B I R D S")

#dataset_type = st.sidebar.selectbox("Prerecorded files",'1')
#image_files_subset = dtype_file_structure_mapping[dataset_type]

#selected_species = st.sidebar.selectbox("Bird Type", '2')


#st.subheader('How does it works:')

#st.subheader("Here is the spectrogram of your recording")
#resized_spectro = spectro#.resize((336,336))
#st.image('/home/benoit/code/benoitdb/birds-frontend/images/spectro.png')
