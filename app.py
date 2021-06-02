#IMPORTS
import os
import streamlit as st
import pandas as pd
import numpy as np
import operator
import soundfile as sf
from IPython.display import Audio
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
    bytesdata = file.read()
    with open("pip.ogg", "wb") as file:
        file.write(bytesdata)

# api call

button = st.button('Identify this Bird !','Submit','Clic to identify this record')
if button:
    url = "https://birdsapi-kkxhmnngqq-ew.a.run.app/uploadfile"
    print("lkjlkj")
    print(bytesdata)
    files = {"file": bytesdata}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        resp = response.json()
        resp
    else:
        "😬 api error 🤖"
        response
        
#st.audio(file, format='audio/ogg')
        
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



# @st.cache()
# def load_index_to_label_dict(path='src/index_to_class_label.json'):
#     """Retrieves and formats the index to class label lookup dictionary needed to 
#     make sense of the predictions. When loaded in, the keys are strings, this also
#     processes those keys to integers."""
#     with open(path, 'r') as f:
#         index_to_class_label_dict = json.load(f)
#     index_to_class_label_dict = {int(k): v for k, v in index_to_class_label_dict.items()}
#     return index_to_class_label_dict

# def load_files_from_s3(keys, bucket_name='bird-classification-bucket'):
#     """Retrieves files anonymously from my public S3 bucket"""
#     s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
#     s3_files = []
#     for key in keys:
#         s3_file_raw = s3.get_object(Bucket=bucket_name, Key=key)
#         s3_file_cleaned = s3_file_raw['Body'].read()
#         s3_file_image = Image.open(BytesIO(s3_file_cleaned))
#         s3_files.append(s3_file_image)
#     return s3_files

# @st.cache()
# def load_all_image_files(path='src/all_image_files.json'):
#     """Retrieves JSON document outining the S3 file structure"""
#     with open(path, 'r') as f:
#         return json.load(f)

# @st.cache()
# def load_list_of_images_available(all_image_files, image_files_dtype, bird_species):
#     """Retrieves list of available images given the current selections"""
#     species_dict = all_image_files.get(image_files_dtype)
#     list_of_files = species_dict.get(bird_species)
#     return list_of_files

# @st.cache()
# def predict(img, index_to_label_dict, model, k):
#     """Transforming input image according to ImageNet paper
#     The Resnet was initially trained on ImageNet dataset
#     and because of the use of transfer learning, I froze all
#     weights and only learned weights on the final layer.
#     The weights of the first layer are still what was
#     used in the ImageNet paper and we need to process
#     the new images just like they did.
    
#     This function transforms the image accordingly,
#     puts it to the necessary device (cpu by default here),
#     feeds the image through the model getting the output tensor,
#     converts that output tensor to probabilities using Softmax,
#     and then extracts and formats the top k predictions."""
#     formatted_predictions = model.predict_proba(img, k, index_to_label_dict)
#     return formatted_predictions

# if __name__ == '__main__':
#     # model = load_model()
#     # index_to_class_label_dict = load_index_to_label_dict()
#     # all_image_files = load_all_image_files()
#     # types_of_birds = sorted(list(all_image_files['test'].keys()))
#     # types_of_birds = [bird.title() for bird in types_of_birds]

#     # dtype_file_structure_mapping = {
#     #     'All Images': 'consolidated', 'Images Used To Train The Model': 'train',
#     #     'Images Used To Tune The Model': 'valid', 'Images The Model Has Never Seen': 'test'
#     #     }
#     # types_of_images = list(dtype_file_structure_mapping.keys())






logo = st.sidebar.image('/home/benoit/code/benoitdb/birds-frontend/images/logo_100px.png')
st.sidebar.subheader("B I R D S")
dataset_type = st.sidebar.selectbox("Prerecorded files",'1')
#image_files_subset = dtype_file_structure_mapping[dataset_type]

selected_species = st.sidebar.selectbox("Bird Type", '2')
#         available_images = load_list_of_images_available(all_image_files, image_files_subset, selected_species.upper())
#         image_name = st.sidebar.selectbox("Image Name", available_images)
#         if image_files_subset == 'consolidated':
#             s3_key_prefix = 'consolidated/consolidated'
#         else:
#             s3_key_prefix = image_files_subset
#         key_path = os.path.join(s3_key_prefix, selected_species.upper(), image_name)
#         files_to_get_from_s3 = [key_path]
#         examples_of_species = np.random.choice(available_images, size=3)
#         for im in examples_of_species:
#             path = os.path.join(s3_key_prefix, selected_species.upper(), im)
#             files_to_get_from_s3.append(path)
#         images_from_s3 = load_files_from_s3(keys=files_to_get_from_s3)
#         img = images_from_s3.pop(0)
#         prediction = predict(img, index_to_class_label_dict, model, 5)

prediction = {'Acrocephalus palustris': 3.1710833e-08, 'Sylvia atricapilla': 2.5642566e-07, 'Hirundo rustica': 0.99999976}
top_prediction = max(prediction.items(), key=operator.itemgetter(1))[0]
top_prediction_rate = max(prediction.items(), key=operator.itemgetter(1))[1]


st.subheader("Here is the most likely bird : ")
st.image('/home/benoit/code/benoitdb/birds-frontend/images/Hirundo_rustica.jpg')
st.title(top_prediction)
st.subheader("With a probability of : " + str(round(top_prediction_rate, 2)))
link = 'https://en.wikipedia.org/wiki/' + top_prediction.lower().replace(' ', '%20')
st.write(f'<a href="{link}" target="_blank">{top_prediction}</a>')


st.subheader("Here are the three most likely bird species")
df = pd.DataFrame(data=np.zeros((3, 2)), 
                    columns=['Species', 'Confidence Level'])


df = pd.DataFrame(columns=['Species', 'Confidence Level'])
for name, prob in prediction.items():
    link = 'https://fr.wikipedia.org/wiki/' + name.lower().replace(' ', '_')
    df.loc[name, 'Species'] = f'<a href="{link}" target="_blank">{name.title()}</a>'
    df.loc[name, 'Confidence Level'] = prob
    
df.reset_index()
df.sort_values(by='Confidence Level', ascending=False)

st.write(df.to_html(escape=False), unsafe_allow_html=True)

#st.subheader('How does it works:')

st.subheader("Here is the spectrogram of your recording")
#resized_spectro = spectro#.resize((336,336))
st.image('/home/benoit/code/benoitdb/birds-frontend/images/spectro.png')
