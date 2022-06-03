import re
import numpy as np

def create_feature(df, column_name, feature_name, pattern):
    feature_pattern=re.compile(pattern, re.IGNORECASE)
    df[feature_name]=(df[column_name].apply(lambda x: feature_pattern.findall(x))).apply(len)
    df[feature_name]=np.where(df[feature_name]>0,feature_name,"")
    return df