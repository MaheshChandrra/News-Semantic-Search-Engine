from flask import Flask, render_template, redirect, app
from flask import request
import pandas as pd
from sentence_transformers import SentenceTransformer
import scipy.spatial
from tqdm import tqdm_notebook
import scipy
import numpy as np
import socket 
import pickle
import random
import numpy as np
import random
from datetime import datetime
import sys
from flask import jsonify
import gdown
import app_config
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


pd.set_option('display.max_colwidth', -1)

@app.route("/")
def index():
    return render_template("main_home_page.html",host=host,port=port)

###############################################################################################################

@app.route('/similarnews', methods=['GET', 'POST'])
def similarnews():
    try:
        response_json={}
        input_news = request.form["input_news"]
        top=int(request.form["top"])
        response_json['Similar_News']=get_similar_news_by_cs(input_news,top)
        df_results = pd.read_json(response_json['Similar_News'])
        table_inner_html=df_results.to_html(classes="table table-bordered table-striped mb-0")
        return render_template("results.html",top=top,input_news=input_news,table_inner_html=table_inner_html)
    except Exception as e:
        return jsonify(input_title_and_abstract=input_news,error=str(e))


###############################################################################################################

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    return render_template("contact_us.html")

###############################################################################################################

@app.route('/get_similar_news', methods=['GET', 'POST'])
def get_similar_news():
    try:
        response_json={}
        input_news = request.args.get('input_title_and_body')
        top=int(request.args.get('top'))
        print(input_news)
        print(top)
        print('#'*100)
        error='None'
        response_json['Similar_News']=get_similar_news_by_cs(input_news,top)
    except Exception as e:
        print(e)
        return jsonify(input_news=input_news)

    return jsonify(input_news=input_news,error=error,Similar_News=response_json['Similar_News'])



###############################################################################################################


### Compose Cosine Similarity and Send back the response

def get_similar_news_by_cs(query,top):
    query_vector=np.array(embedder.encode([query],show_progress_bar=False),dtype='float32')

    
    ###Caliculation of Cosine Similarity
    top_n_records=top

    df_main=df.copy()
    
    embeddings=df_main['embeddings'].values.tolist()
    queries=[query]
    query_embeddings=[query_vector]
    df_main['Cosine Similarity']=-1
    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist(query_embedding, embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        closest_n=top_n_records
        print("Abstract:\n",query)
        for idx, distance in results[0:closest_n]:
            df_main['Cosine Similarity'][idx]=(1-distance)
            
    ###Sort Values by Cosine Similarity
    df_main=df_main.sort_values(by=['Cosine Similarity'],ascending=False).reset_index(drop=True)
    df_main=df_main[0:top]
    df_main=df_main[['link', 'headline', 'category', 'short_description', 'authors', 'date','headline_and_sd','Cosine Similarity']]
    df_main=df_main.rename(columns={'headline_and_sd': 'News'})
    #df_main=df_main[['News','Cosine Similarity']].to_json(orient='records')
    df_main=df_main.to_json(orient='records')

    
    ###Send JSON Results back
    return df_main


###############################################################################################################3



if __name__ == "__main__":
    print("Inside main")
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host= s.getsockname()[0]
    port=8080

    ###Downloading the dataset from google drive
    output = app_config.DATASET_PATH+app_config.DATSET_FILE_NAME

    if not app_config.DATSET_FILE_NAME in os.listdir(app_config.DATASET_PATH):
        gdown.download(app_config.DATASET_DRIVE_LINK, output, quiet=False)
    df=pd.read_pickle(app_config.DATASET_PATH+app_config.DATSET_FILE_NAME)

    
    ###Loading Sentence Embedder
    
    embedder = SentenceTransformer("distiluse-base-multilingual-cased-v2")

    ##############################################################
    app.run(host=host, port=port, debug=False,use_reloader=False)