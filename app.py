from flask import Flask, jsonify
# from flask import Flask, jsonify, request
from flasgger import Swagger
import pickle as pickle
# import numpy as np
import pandas as pd
# import json as json

# data = pd.read_csv('static/final_data.csv')
# filtered_data = data[['product_id','category_id','price','user_id','is_purchased','product_name']]
# purchase_count = pd.DataFrame(filtered_data.groupby('product_id')['is_purchased'].mean())
# purchase_count['purchased times'] = pd.DataFrame(filtered_data.groupby('product_id')['is_purchased'].count())

app = Flask(__name__)
Swagger(app)

@app.route("/")
def helloWorld():
    return "Hello World"

@app.route("/input/<int:productID>", methods=['POST'])
def predict(productID):
    loaded_model_map = pickle.load(open('static/ProductMap.sav', 'rb'))
    product1_purchasing = loaded_model_map[productID]
    similar_to_product1 = loaded_model_map.corrwith(product1_purchasing).dropna()
    corr_product1 = pd.DataFrame(similar_to_product1,columns=['Correlation'])
    # corr_product1 = corr_product1.join(purchase_count['purchased times'])
    # corr_product1_result = corr_product1[(corr_product1['Correlation']>0.6) | (corr_product1['Correlation']<0.2) & (corr_product1['Correlation']>=0)].sort_values('Correlation', ascending=False)
    corr_product1_result = corr_product1[(corr_product1['Correlation']>=0)].sort_values('Correlation', ascending=False)
    final_data = corr_product1_result.reset_index()
    dict = final_data.to_dict('index')
    return jsonify(dict)

app.run(port=5000)