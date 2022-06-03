import joblib
from tensorflow import keras
import DataCleaning as DC
import pandas as pd
import pickle
from keras.preprocessing.sequence import pad_sequences
import time
import numpy as np
from datetime import datetime
import os


def Classifier(path, working_dir, save_folder_path):
    start_datetime = datetime.now()  # current date and time
    start_datetime = start_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    start = time.time()
    df_original = pd.read_csv(path, encoding='ISO-8859-1')
    df = pd.DataFrame(DC.DataCleaning(path))
    corpus = list(df['text'].str.split(' ', expand=False))
    corpus_svm = df['text'].to_numpy()

    ##### 1a. Loading W2V and fastText tokenizer
    # loading tokenizer
    with open(working_dir + '//Dependencies//tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    maxlen = 300
    X_test = tokenizer.texts_to_sequences(corpus)
    X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

    ##### 1b. Preparing data for SVM model
    # loading tf-idf vectorizer
    with open(working_dir + '//Dependencies//Tfidf_vectorizer.pickle', 'rb') as handle:
        Tfidf_vectorizer = pickle.load(handle)

    X_test_Tfidf = Tfidf_vectorizer.transform(corpus_svm)

    ### 2. Loading Models
    svm_model = joblib.load(working_dir + '//Dependencies//SVM-model.pkl')
    w2v_model = keras.models.load_model(working_dir + '//Dependencies//CNN-model-Word2Vec_adam.h5')
    ft_model = keras.models.load_model(working_dir + '//Dependencies//CNN-model-FastText_adam.h5')
    ### 3. Performing predictions
    w2v_pred = w2v_model.predict(X_test)[:, 0]
    ft_pred = ft_model.predict(X_test)[:, 0]
    svm_pred = svm_model.predict_proba(X_test_Tfidf)[:, 1]
    ### 4. Output Predictions
    output = pd.DataFrame({'SVM': svm_pred, 'CNN-Word2Vec': w2v_pred, 'CNN-FastText': ft_pred})
    output['Ensemble'] = output[['SVM', 'CNN-Word2Vec', 'CNN-FastText']].mean(axis=1)
    output['Prediction'] = np.where(output['Ensemble'] < 0.05, 0, 1)

    output1 = pd.concat([df_original, output], axis=1)

    end = time.time()

    # increment file name if it exists

    if os.path.exists(save_folder_path + '//ClassifiedCRTs.csv'):
        i = 1
        if os.path.exists(save_folder_path + f'//ClassifiedCRTs(1).csv'):
            while os.path.exists(save_folder_path + f'//ClassifiedCRTs({i}).csv'):
                i += 1
                file_name = save_folder_path + f'//ClassifiedCRTs({i}).csv'
        else:
            file_name = save_folder_path + f'//ClassifiedCRTs(1).csv'
    else:
        file_name = save_folder_path + '//ClassifiedCRTs.csv'
    print('My file name is:', file_name)
    output1.to_csv(file_name)
    print(f'Classification Completed in {end - start} seconds')
    saved_path = file_name
    saved_path = saved_path.replace("//", "\\")
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    my_label=f'[color=000000]Classification finished: {date_time}.\n' \
             f'The file path was copied to your clipboard and your file is saved here:\n[b]{saved_path}[/color][/b]'
    return my_label, saved_path
