""" This is a content-based recommender system for cosmetic products. With this recommendation system, customers can find other products similar in category and ingredients with the one they are using or intend to use. """

# import libraries
# pip install rake_nltk first to use Rake package
import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

""" Create a dataframe with the columns I want to use in my recommender system. """
df_doc = df[["Label", "brand","name", "ingredients"]]

""" Extracting key words from ingredients and give them weights based on their importance.""" 
# initializing the new column
df_doc['Key_words'] = ""

for index, row in df_doc.iterrows():
    ingredients = row['ingredients']
    
    # instantiating Rake, by default it uses english stopwords from NLTK
    # and discards all puntuation characters as well
    r = Rake()

    # extracting the words by passing the text
    r.extract_keywords_from_text(ingredients)

    # getting the dictionary whith key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()
    
    # assigning the key words to the new column for the corresponding products
    row['Key_words'] = list(key_words_dict_scores.keys())

# dropping the ingredients column
df_doc.drop(columns = ['ingredients'], inplace = True)


""" Include brand name and category of the products."""
# lower brands' names
df_doc['brand'] = df_doc['brand'].map(lambda x: x.lower())

df_doc['Label'] = df_doc['Label'].map(lambda x: x.lower())

"""Set products' names as index."""
df_doc.set_index('name', inplace = True)
df_doc.head()

"""Create a bag of words."""
df_doc['bag_of_words'] = ''
columns = df_doc.columns
for index, row in df_doc.iterrows():
    words = ''
    for col in columns:
        if col != 'brand':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
df_doc.drop(columns = [col for col in df_doc.columns if col!= 'bag_of_words'], inplace = True)

"""Generalise a matrix and calculate the cosine similarity of products."""
# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df_doc['bag_of_words'])

# generating the cosine  similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(df_doc.index)
indices[:5]

"""Create a function to recommend top 10 closest products."""
# function that takes in product title as input and returns the top 10 recommended products
def recommendations(title, cosine_sim = cosine_sim):
    
    recommended_products = []
    
    # gettin the index of the products that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar products
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching products
    for i in top_10_indexes:
        recommended_products.append(list(df_doc.index)[i])
        
    return recommended_products