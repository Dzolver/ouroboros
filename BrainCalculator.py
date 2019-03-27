import os
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

    def generate_object_name(self,object_name,sentence):
        print("generating object name...")
        POSTagList = st.tag(word_tokenize(sentence))
        print(POSTagList)
        for item in POSTagList:
            print(item[0])
        return self

    def justTAG(self,sentence):
        return st.tag(word_tokenize(sentence))

    def generate_detail_name(self):
        print("generating detail name...")
        return self

    def generate_branch_level(self):
        print("generating branch level...")
        return self

    def generate_personality_score(self):
        print("generating personality score...")
        return self

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