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
_path_to_tree = 'localTree.txt'
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

    def generate_branch_level(self):
        print("generating branch level...")
        return self

    #this function finds the most prominent object in the users input by comparing position and POS Tags
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
        elif str(local_candidate) == 'Byung' or str(local_candidate) == 'I':
            primary_object_candidate = 'USER'
        else:
            primary_object_candidate = local_candidate
        #tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        #tfidf_transformer.fit(word_count_vector)
        #tfidf_vector = tfidf_transformer.transform(cv.transform([wordList]))
        #sorted_items = self.sort_coo(tfidf_vector.tocoo())
        POSTagList = st.tag(word_tokenize(sentence))
        print(POSTagList)
        for item in POSTagList:
            print(item[0])
        return primary_object_candidate

    #this function generates the personal score that defines how personal a sentence is, to the user.
    def generate_personality_score(self,personal_array):
        print("generating personality score...")
        #calculations to deem personal score based on initial score values and position
        #the closer towards the head AND tail, the better
        final_p_score = 0
        p_score_pos_array = []
        #length of sentence, position of scores, scores itself
        for p_score in personal_array:
            p_score_pos_array.append(p_score)
        pos = 0
        for p_score_pos in p_score_pos_array:
            print("POINTS : " + str(p_score_pos))
            length = len(p_score_pos_array)
            offset = (pos%length/2)
            if pos == len(p_score_pos_array) - 1 :
                offset = (length/2)
            final_p_score += (((pos * -1) + length/2 + 1 + offset) * 0.1 * p_score_pos)
            pos += 1
        return final_p_score

    #this function generates a score of familiarity based on how many matches are found within the local storage
    def generate_fam_score(self, sentence):
        print("generating understanding score...")
        fam_score = -5
        offset = 0
        with open(_path_to_tree,'r') as t:
            lines = t.readlines()
            for component in sentence.split(" "):
                for line in lines:
                    for micro_line in line.split(":"):
                        if component in line:
                            offset += 1
        fam_score = fam_score + offset/4
        t.close()
        return fam_score

    #this function generates a scsore that acts a metric for the program to know little it knows of a detail
    def generate_unknown_score(self,detail,detail_array):
        unknown_score = 10
        count = 0
        offset = 0
        print("generating unknown score...")
        lineNum, object_presence = self.check_object_node(detail)
        if object_presence == True:
            offset = 2
            object_presence_detail_count, detailLineNum, object_presence_detail_array = self.check_object_details(lineNum)
            offset = offset*object_presence_detail_count

        if len(detail_array) == 0:
            count = 0
        else:
            for detail_node in detail_array:
                if detail_node == detail:
                    count += 1

        unknown_score = unknown_score - (offset + count * 1.5)
        return unknown_score

    def justTAG(self,sentence):
        return st.tag(word_tokenize(sentence))

    def getSentenceLength(self,sentence):
        words = sentence.split(" ")
        return len(words)

    def check_object_details(self,objLineNum):
        detailLineNum = 0 #the last detail line number of that specific object - more efficient than re-iterating
        count = 0
        found = False
        detail_array = []
        with open("localTree.txt","r") as t:
            print("checking for object details...")
            lastDetail = 1
            for i,line in enumerate(t):
                if line.strip() and found and i != objLineNum - 2:
                    detail_name = (self.detailComponentRetriever(2,line.strip())).split(':')[1]
                    detail_array.append(detail_name)
                    count += 1
                    lastDetail = lastDetail + i
                    print("B LINE NUMBER " + str(i + 1) + " " + line)
                    detailLineNum += 1
                    continue
                if line.strip() and i == objLineNum-2:
                    found = True
                    print("Line Number : " + str(objLineNum-1) + " | OBJ FOUND : " + line)
                    detailLineNum += 1
                    continue
                elif not line.strip() and found:
                    break
                elif not line.strip() and not found:
                    detailLineNum += 1
                    continue
                elif line.strip() and not found:
                    detailLineNum += 1
                    continue
        print(detail_array)
        t.close()
        return count, detailLineNum, detail_array

    def detailComponentRetriever(self,componentNumber,line):
        component = line.split(',')[componentNumber-1]
        print("THIS IS A COMPONENT " + str(component))
        return component

    def rawTextFinder(self,componentNumber,line):
        component = ""
        for i, componentRaw in enumerate(line):
            if i+1 == componentNumber:
                component = (componentRaw.split(":"))[1]
        return component

    def check_object_node(self,object_name):
        objfound = False
        with open("localTree.txt","r") as t:
            target = "ObjectName:" + object_name
            lineNum = 0
            for line in t:
                lineNum += 1
                if target in str(line):
                    objfound = True
                    break
                else:
                    objfound = False
                    continue
        t.close()
        if lineNum != 0:
            lineNum += 1
        return lineNum,objfound

    def get_object_line(self,object_name):
        with open("localTree.txt","r") as t:
            target = "ObjectName:" + object_name
            line_num = 0
            for line in t:
                line_num += 1
                if target in str(line):
                    break
                else:
                    continue
        t.close()
        if line_num != 0:
            line_num += 1
        return line_num

    def find_object_node(self, object_name):
        objfound = False
        with open("localTree.txt", "r") as t:
            target = "ObjectName:" + object_name
            for line in t:
                if target in str(line):
                    objfound = True
                    break
                else:
                    objfound = False
                    continue
        t.close()
        return objfound

    def generate_sentiment_score(self,sentence):
        nltk_sentiment = SentimentIntensityAnalyzer()
        sentiment_score = nltk_sentiment.polarity_scores(sentence)
        print("generating semantic score...")
        return sentiment_score

    def remember_details(self,intent,existing_objects):
        all_details = []
        for existing_object in existing_objects:
            count, detail_line_num, detail_array = self.check_object_details(self.get_object_line(existing_object))
            all_details += detail_array
        print("ALL DETAILS")

    def generate_response(self,sentence,object_name,detail_name,question,p_score,f_score,u_score,s_score,detail_array):
        response = ""
        object_score = 0
        detail_score = 0
        statement_score = 0
        question_score = 0
        pronoun_pool = []
        noun_pool = []
        adjectives_pool = []
        connector_pool = []
        verb_pool=[]
        past_verb_pool=[]
        simple_verb_pool=[]
        VRB_pool=[]
        rb_pool=[]
        MD_pool = []
        WRB_pool = []
        WP_pool = []
        #multi-dimensional array
        word_bank = []
        if self.find_object_node(object_name):
            print("Previous object found!")
            object_score += 1

        for entry in self.justTAG(sentence):
            pos = entry[0]
            tag = entry[1]
            if tag == 'NN':#NOUNS
                noun_pool.append(pos)
                continue
            elif tag == 'NNS': #NOUNS PLURAL
                noun_pool.append(pos)
                continue
            elif tag == 'NNP':#unidentified pronoun
                pronoun_pool.append(pos)
                continue
            elif tag == 'JJ':#ADJECTIVES
                adjectives_pool.append(pos)
                continue
            elif tag =='VBP':#VERB
                verb_pool.append(pos)
                continue
            elif tag == 'VRB':
                if pos == "do" and question:
                    WP_pool.append(pos)
                else:
                    VRB_pool.append(pos)
                continue
            elif tag == 'VB':
                simple_verb_pool.append(pos)
                continue
            elif tag == 'VBD':
                past_verb_pool.append(pos)
                continue
            elif tag == 'VBG':
                verb_pool.append(pos)
                continue
            elif tag == 'VBZ':
                verb_pool.append(pos)
                continue
            elif tag == 'RB': #Example : do you STILL like me ?
                rb_pool.append(pos)
                continue
            elif tag == 'MD':
                MD_pool.append(pos)
                continue
            elif tag == 'WRB':
                WRB_pool.append(pos)
                continue
            elif tag == 'WP':
                WP_pool.append(pos)
                continue
            else:
                continue
        print("PRONOUNS " + str(pronoun_pool))
        print("NOUNS " + str(noun_pool))
        print("ADJECTIVES " + str(adjectives_pool))
        print("VERBS " + str(verb_pool))
        print("SIMPLE VERBS" + str(simple_verb_pool))
        print("PAST VERBS " +str(past_verb_pool))
        print("RB " + str(rb_pool))
        print("VRB " + str(VRB_pool))
        print("WRB " + str(WRB_pool))
        print("MD" + str(MD_pool))
        print("WP " + str(WP_pool))
        existing_objects=dict()
        detail_count = 0
        line_num = 0
        detail_array = []
        noun_scores = dict()
        for word in pronoun_pool:
            if self.find_object_node(word):
                total_score = 2
                detail_count,line_num,detail_array = self.check_object_details(self.get_object_line(word))
                existing_objects[word] = detail_count
                if word == object_name:
                    total_score = total_score*3
                total_score = total_score * detail_count
                noun_scores[word] = total_score
            else:
                continue
        for word in noun_pool:
            print('word:'+word)
            if self.find_object_node(word):
                total_score = 2
                detail_count,line_num,detail_array = self.check_object_details(self.get_object_line(word))
                existing_objects[word] = detail_count
                if word == object_name:
                    total_score = total_score*3
                total_score = total_score * detail_count
                noun_scores[word] = total_score
        print("Existing objects" + str(existing_objects))
        local_memory = self.get_local_memory(noun_pool)
        print('LOCAL MEMORY = ' + str(local_memory))
        if question:
            #get all segments from wrb,md, wp
            banana_split = sentence.split(" ")
            i = len(banana_split)
            banana_max = 0
            target_question = ""
            for word in banana_split:
                if word in WRB_pool or word in MD_pool or word in WP_pool:
                    banana_max = i
                    target_question = word
                    break
            print("TARGET QUESTION : " + target_question)
            local_memory = self.get_local_memory(noun_pool)
            print('LOCAL MEMORY = ' + str(local_memory))
            return response
        elif not question:
            return response

    def get_local_memory(self,noun_pool):
        #for word in noun_pool:
        #access the storage and return
        #all memories that have relevance to the input sentence in terms of
            #1. Matching object names and all their details
            #2. Matching detail names in other objects
        with open('localTree.txt','r') as t:
            print("NOUN POOL : " + str(noun_pool))
            local_memory = []
            all_lines = t.readlines()
            for i,line in enumerate(all_lines):
                lineNum = i + 1
                #print("THIS IS PRINTED:" + str(self.detailComponentRetriever(4, line.strip())).split(':')[1])
                print(line)
                if "ObjectName:" in line:
                    continue
                elif line == "":
                    continue
                else:
                    component = self.rawTextFinder(4,(line.strip()).split(","))
                    print(str("THIS IS THE COMPONENT:" + component))
                    for word in noun_pool:
                        if word.lower() in component.lower():
                            local_memory.append(component)
                            break
        return local_memory

    def get_server_memory(self):
        return self

    def has_enough_knowledge(self):
        return self

    def get_total_memory(self):
        return self

    def create_word_bank(self):
        return self

    def connect_components(self):
        return self

    def component_election(self):
        return self

    def create_raw_response(self):
        return self

    def fine_tune_response(self):
        return self