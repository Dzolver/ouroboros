import os
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


java_path = "C:/Program Files/Java/jdk-12/bin/java.exe"
os.environ['JAVAHOME'] = java_path
os.environ['CLASSPATH'] = "stanford-pos"
os.environ['STANFORD_MODELS'] = "stanford-pos"
_path_to_model = 'stanfordPOSTagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = 'stanfordPOSTagger/stanford-postagger.jar'

from nltk.tag import StanfordPOSTagger

st = StanfordPOSTagger(_path_to_model,_path_to_jar,encoding='utf8')

class BrainCalculator:
    object_name = ""
    detail_name = ""
    branch_level = 0
    personality_score = 0
    understanding_score = 0
    unknown_score = 0
    sentence = ""
    semantic_score = 0

    def __init__(self,object_name,detail_name,branch_level,personality_score,understanding_score,unknown_score,sentence,semantic_score):
        self.object_name = object_name
        self.detail_name = detail_name
        self.branch_level = branch_level
        self.personality_score = personality_score
        self.understanding_score = understanding_score
        self.unknown_score = unknown_score
        self.sentence = sentence
        self.semantic_score = semantic_score

    def get_stop_words(self,stop_file_path):
        with open(stop_file_path,'r',encoding="utf-8") as f:
            stopwords = f.readlines()
            stop_set = set(m.strip() for m in stopwords)
            return stop_set

    def generate_object_candidates(self,sentence,local_candidate):
        primary_object_candidate = ""
        print("generating object candidates...")
        wordList = sentence.split(' ')
        stopwords = self.get_stop_words("resources/stopwords.txt")
        cv = CountVectorizer(max_df=0.85,stop_words=stopwords)
        word_count_vector = cv.fit_transform(wordList)
        print(word_count_vector)
        candidates = list(cv.vocabulary_.keys())[:10]
        if local_candidate in candidates:
            print(local_candidate + " IS THE OBJECT WE NEED!")
            primary_object_candidate = local_candidate
        elif str(local_candidate).lower() == 'byung':
            primary_object_candidate = 'USER'
        #tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        #tfidf_transformer.fit(word_count_vector)
        #tfidf_vector = tfidf_transformer.transform(cv.transform([wordList]))
        #sorted_items = self.sort_coo(tfidf_vector.tocoo())
        POSTagList = st.tag(word_tokenize(sentence))
        print(POSTagList)
        for item in POSTagList:
            print(item[0])
        return self,primary_object_candidate

    def justTAG(self,sentence):
        return st.tag(word_tokenize(sentence))

    #This function is no longer needed, as it is implemented in 3-14.py line 151
    def generate_detail_name(self,sentence,local_candidate):
        print("generating detail name...")
        wordList = sentence.split(' ')
        stopwords = self.get_stop_words("resources/stopwords.txt")
        cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
        word_count_vector = cv.fit_transform(wordList)
        print(word_count_vector)
        candidates = list(cv.vocabulary_.keys())[:10]
        if local_candidate in candidates:
            print(local_candidate + " IS THE OBJECT WE NEED!")
            primary_object_candidate = local_candidate
        return self

    def generate_branch_level(self):
        print("generating branch level...")
        return self

    def generate_personality_score(self,personal_array):
        print("generating personality score...")
        #calculations to deem personal score based on initial score values and position
        #the closer towards the head AND tail, the better
        final_p_score = 0
        p_score_pos_array = []
        #length of sentence, position of scores, scores itself
        for p_score in personal_array:
            p_score_pos_array.append(p_score)
        p_booster_rule = 5.0
        p_booster = p_booster_rule/len(p_score_pos_array)
        pos = 0
        for p_score_pos in p_score_pos_array:
            print("POINTS : " + str(p_score_pos))
            length = len(p_score_pos_array)
            balancer = (pos%length/2)
            if pos == len(p_score_pos_array) - 1 :
                balancer = (length/2)
            final_p_score += (((pos * -1) + length/2 + 1 + balancer) *0.1* p_score_pos)
            pos += 1
        return final_p_score

    def generate_understanding_score(self):
        print("generating understanding score...")
        return self

    def generate_unknown_score(self):
        print("generating unknown score...")
        return self

    def generate_semantic_score(self,sentence):
        nltk_sentiment = SentimentIntensityAnalyzer()
        sentiment_score = nltk_sentiment.polarity_scores(sentence)
        print("generating semantic score...")
        return sentiment_score