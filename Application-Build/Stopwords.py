def stopwords():
    stopwords=['few', 've', 'was', 'am', 'm', 'whom', 'be', 'which', 'only', 'been', 'won', "hasn't", 'isn',
               'are', 'her', 'hers', "doesn't", 'itself', 'but', 'or', "you're", 'further', 'about', "needn't",
               "didn't", 'to', 'more', 'so', 'from', 'most', "mustn't", 'because', 'after', 'above', 'shan', 'very',
               'all', "should've", 'some', 'then', 'hasn', "hadn't", 'below', 'during', 'had', 'having', 'his',
               'my', 'did', 'here', 'such', 'ours', "couldn't", "weren't", 'up', 'weren', "haven't", 'mightn', 'down',
               'there', 'aren', 'against', 'both', 'this', 'that', 'yourselves', 'doesn', 'were', "isn't", 'where',
               'have', 'not', 'haven', 'those', 'as', 'between', 'o', 'other', 'theirs', 'mustn', 'while', 'in', 'him',
               'through', 'he', 'we', 'is', 'themselves', 'once', 'couldn', 'no', 'do', "she's", 'them', 'when', 's',
               "that'll", "it's", 'doing', 'should', 'too', 'off', 'who', 'hadn', 'nor', 'ain', "you've", 'you', 'yourself'
               , 'ma', 'these', 'd', 'it', 'what', "aren't", "don't", "wouldn't", 'at', "shouldn't", 'over', 'own',
               "you'll", 'why', 'into', 'wasn', 'with', 'she', 'any', 'now', 'herself', 'and', 'ourselves', 'under',
               'll', 'a', "mightn't", "shan't", 'an', 'don', 'they', 'each', 'does', 're', 'their', 'has', 'than',
               'just', 'until', 'will', 'y', 'of', 'before', 'shouldn', 'how', 'for', 'out', 'wouldn', 'by', 'our',
               'needn', "won't", 'on', 'didn', "you'd", 'if', 'the', 'can', 'yours', 'its', 't', 'i', 'himself',
               'being', 'again', 'me', 'myself', 'same', 'your', "wasn't"]
    newStopWords = ['aim','background','methods','results','discussion','conclusion', 'conclusions','limitations',
                    'limitation','stopnow']
    stopwords.extend(newStopWords)
    return stopwords