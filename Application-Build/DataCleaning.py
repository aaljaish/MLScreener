import pandas as pd
import CleanText as ct
import Stopwords as stopwords
import CreateFeature as cf
stopwords=stopwords.stopwords()
import re


def DataCleaning(csv_path):
    # Read in dataframe
# Read in dataframe
    df=pd.read_csv(csv_path, encoding='ISO-8859-1')
    df=df[['TI','AB','KW','MH']]
    df.fillna("",inplace=True)
    df["Stop"]="stopnow"
    df2=pd.DataFrame({"text": df.apply(lambda x: ','.join(x.astype(str)), axis=1)})

    # make lowercase, remove text in brackets, words with numbers, digits, newlines, 
    # single letter words, double spaces, randomis --> randomiz, centre --> center
    round1 = lambda x: ct.clean_text_step1(x)  

    # remove all text starting at the "conclusion" or "discussion" sections.
    round2 = lambda x: ct.clean_text_step2(x)

    # Remove punctuation.
    round3 = lambda x: ct.clean_text_step3(x)
    
    df3=df2.text.apply(round1)
    df4=pd.DataFrame({'text': df3})

    df4=pd.DataFrame({'text': df4.text.apply(round2)})
    df4=pd.DataFrame({'text': df4.text.apply(round3)})

    df4=cf.create_feature(df=df4,column_name='text',feature_name='step_wedged', pattern='stepped[- ]wedge|step[- ]wedge')
    df4=cf.create_feature(df=df4,column_name='text',feature_name='cluster_design', pattern="((cluster[- ]+([^:. \n]+[- ]+){0,5}([t][r][ai][ai][l]|RCT|study|experiment|intervention)))")
    df4=cf.create_feature(df=df4,column_name='text',feature_name='cluster_randomized_one', pattern="((pre)?school(s|room|rooms)?|class(es|room|rooms)?|cluster|communit(y|ies)?|village(s)?|church(es)?|worksite(s)?|practices)([- ]+([^:. \n]+[- ]){0,5})([t][r][ai][ai][l]|RCT|random|allocat|cluster|intervention)")
    df4=cf.create_feature(df=df4,column_name='text',feature_name='cluster_randomized_two', pattern="((RCT|assign(ed|s|ing|ment)?|random(ly|ize|ized|ise|isation|ization)?|cluster(s|ing)?)([- ]([^:. ]+[- ]){0,5})((pre)?school|class|communit|village|church|worksite|practice))")
    df4=cf.create_feature(df=df4,column_name='text',feature_name='participant_randomized', pattern="(adults|men|women|kids|children|patients|subjects|participants)[- ]([^:. \n:]+[- ]){0,3}(random|assign)")
    
    df4['text2']=pd.DataFrame({"text1": df4[['step_wedged','cluster_design','cluster_randomized_one','cluster_randomized_two','participant_randomized','text']].apply(
    lambda x: ' '.join(x.astype(str)), axis=1)})
    
    df5= df4['text2'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
    df5=pd.DataFrame({'text': df5.apply(round2)})
    
    return df5['text']