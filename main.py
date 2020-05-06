import pandas as pd
import string
import nltk as nlp
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import collections
import math
import time
data=pd.read_csv('hotel-reviews/7282_1.csv')

def see_info(ds):
    #print information of data set
    print(ds.info())
    print(ds.nan)
    #print few data from reviews text
    print(ds['reviews.text'].head())
    print(ds['reviews.text'].tail())

#copy all reviews to a variable
reviews=data['reviews.text']
#remove last row as it's not important
reviews.pop(len(data)-1)




def remove_stop_words(text):
    new_token=[]
    s_words=set(stopwords.words('english'))
    text=text.lower()
    tokens=word_tokenize(text)
    for i in tokens:
        if i not in s_words and i.isalpha():
            new_token.append(i)
    return new_token



def find_tf_string(token_list):
    weight_dict=collections.Counter(token_list)
    tf_dict={}
    for word,weight in zip(weight_dict.keys(),weight_dict.values()):
        tf_dict[word]=(weight/len(token_list))
    return tf_dict

#find tf value for all reviews
def find_tf_list(reviews_list):
    all_tf=[]
    for i in reviews:
        if(type(i) == str):#to avoid all nan values
            all_tf.append(find_tf_string(remove_stop_words(i)))
    return all_tf


def find_idf(tf_list):
    doc_num=len(tf_list)
    idf_list=[]
    idf_dict={}
    for tf_dic in tf_list:
        count=0 #word's occurence counter
        for word in tf_dic.keys():
            for i in tf_list:
                if word in i:
                    count=count+1
            idf_val=math.log(doc_num/count) #idf value for 'word'
            idf_dict[word]=idf_val
            print(word,':',idf_val)
        idf_list.append(idf_dict)
    return idf_list

print("Process Started At:",time.ctime())
#step1. tokenization by removing stop words and punctions from text
tf_list=find_tf_list(reviews)
print('Tf list calculated, calculating idf')
#step2. find idf from tf list
idf_list=find_idf(tf_list)
print("Process finished At:,",time.ctime())
opf=open('idf_list.txt','wb')
opf.write(tf_list)
opf.close()
