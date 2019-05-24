import os
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import requests
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
import language_check
import json
import flaskBoi
import webbrowser
import grammar_check
from language_check import LanguageTool
from nltk import bigrams
import operator

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
    global_noun_pool = []
    question = False
    tool = language_check.LanguageTool('en-US')

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
        self.question = question
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
        self.global_noun_pool = noun_pool
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
        server_memory = self.get_server_memory()
        total_memory = self.get_total_memory(local_memory,server_memory)
        print('LOCAL MEMORY = ' + str(local_memory))
        print('SERVER MEMORY = ' + str(server_memory))
        print('TOTAL MEMORY = ' + str(total_memory))
        generated_word_bank = self.create_word_bank(total_memory)
        print('WORD BANK : ' + str(generated_word_bank))
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
            pronouns = []
            nouns = []
            verbs = []
            adjectives = []
            wrb = []
            final_word_bank = self.apply_weights(generated_word_bank,question,sentence,object_name,detail_name)
            #segment everything into question words, nouns and verbs
            question_starters = ['Did','How','When','Where','How','Can','Is','What','Should','Could','Would']
            wp = ['Who','What']
            wdt = ['Which']
            wp_doll = ['Whose']
            wrb = ['Where','When','How']
            md = ['Can','Could','Will','Should','Would']
            q_connect = ['Was','Did','Is']
            q_connect_2 = ['An','A','It']

            q_past = []
            q_present = [wdt]
            q_future = [md]
            q_pro = [wp,wp_doll]
            q_where = [wrb]
            self_perspective = False
            reverse_perspective = False
            sentence_bank = []

            if 'I' in sentence.split(" "):
                self_perspective = True
                pronouns.append('I')
            if len(final_word_bank[0]) != 0:
                pronouns = final_word_bank[0]
                sentence_bank.append(pronouns)
            if len(final_word_bank[1]) != 0:
                nouns = final_word_bank[1]
                sentence_bank.append(nouns)
            if len(final_word_bank[2]) != 0:
                verbs = final_word_bank[2]
                sentence_bank.append(verbs)
            if len(final_word_bank[3]) != 0:
                adjectives = final_word_bank[3]
                sentence_bank.append(adjectives)
            if len(final_word_bank[6]) != 0:
                for verb in final_word_bank[6]:
                    verbs.append(WordNetLemmatizer().lemmatize(verb,'v'))
                sentence_bank.append(verbs)
            if len(final_word_bank[7]) != 0:
                for verb in final_word_bank[7]:
                    verbs.append(WordNetLemmatizer().lemmatize(verb,'v'))
                sentence_bank.append(verb)
            if len(final_word_bank[9]) != 0:
                wrb = final_word_bank[9]
                sentence_bank.append(wrb)
            print(pronouns)
            print(verbs)
            print(nouns)
            print(adjectives)
            print(wrb)

            sentence_RAW = str(pronouns[0] + " "+ verbs[0] + " "+nouns[0])
            matches = self.tool.check(sentence_RAW)
            print(matches)
            print(language_check.correct(sentence_RAW,matches))
            sentence_tier2 = []
            for i,question_starter in enumerate(question_starters):
                sentence_tier2.append(question_starters[i]+ " " + sentence_RAW)
            print(sentence_tier2)
            tool = grammar_check.LanguageTool('en-GB')
            matches = tool.check(str(sentence_tier2[0]))
            print(matches)
            print(grammar_check.correct(str(sentence_tier2[0]), matches))
            print(self.get_sentence_tense(self.justTAG(sentence)))
            #assign gravity to each set
            #combine set gravities into composite gravities for noun verb pairs
            #combine set gravities into composite gravities for question noun verb triplets
            #filter out final gravity sequence
            return response
    def get_sentence_tense(self,sentencePOSTag):
        tenses = dict()
        present = 0
        past = 0
        future = 0
        for pos,tag in sentencePOSTag:
            if tag == 'VBP' or tag == 'VBG' or tag == 'VBZ' or tag == 'VB':
                present += 1
            elif tag == 'VBN' or tag == 'VBD':
                past += 1
        tenses = {'past':past,'present':present,'future':future}
        return max(tenses.items(),key=operator.itemgetter(1))[0]

    def get_local_memory(self,noun_pool):
        #for word in noun_pool:
        #access the storage and return
        #all memories that have relevance to the input sentence in terms of
            #1. Matching object names and all their details
            #2. Matching detail names in other objects
        with open('localTree.txt','r') as t:
            local_memory = []
            all_lines = t.readlines()
            for i,line in enumerate(all_lines):
                #print("THIS IS PRINTED:" + str(self.detailComponentRetriever(4, line.strip())).split(':')[1])
                if "ObjectName:" in line:
                    continue
                elif line == "":
                    continue
                else:
                    component = self.rawTextFinder(4,(line.strip()).split(","))
                    for word in noun_pool:
                        if word.lower() in component.lower():
                            local_memory.append(component)
                            break
        return local_memory

    def get_server_memory(self):
        print("RUNNING SERVER MEMORY FUNCTION!")
        payload = {'noun_pool':self.global_noun_pool}
        URL = "http://127.0.0.1:5000/remember"
        r = requests.get(url=URL,params=payload)
        server_memory = r.text
        split1 = server_memory.split(',')
        print("SPLIT1:" + str(split1))
        print(split1[0])
        split2 = []
        for split in split1:
            if len(split1) == 0:
                split2 = []
                break
            elif split1[0] == '[]':
                split2 = []
                break
            else:
                split2.append(split.split("'")[1])
        print("SPLIT2:" + str(split2))
        final_server_memory = split2
        #os.system('python -m webbrowser -t "http://127.0.0.1:5000/remember/"')
        #os.system('python flaskBoi.py')
        return final_server_memory

    def get_total_memory(self,local_memory,server_memory):
        total_memory = []
        for i,memory in enumerate(local_memory):
            for j, smemory in enumerate(server_memory):
                if memory == smemory:
                    total_memory.append(memory)
                    local_memory.pop(i)
                    server_memory.pop(j)
                    break
                else:
                    continue
        total_memory = total_memory + local_memory
        total_memory = total_memory + server_memory
        total_memory = list(dict.fromkeys(total_memory))
        return total_memory

    def has_enough_knowledge(self):
        return self

    def create_word_bank(self,total_memory):
        word_bank = []
        pronoun_pool = []
        noun_pool = []
        adjectives_pool = []
        verb_pool=[]
        past_verb_pool=[]
        simple_verb_pool=[]
        VRB_pool= []
        rb_pool= []
        MD_pool = []
        WRB_pool = []
        WP_pool = []
        for memory in total_memory:
            for entry in self.justTAG(memory):
                pos = entry[0]
                tag = entry[1]
                if tag == 'NN':  # NOUNS
                    if pos in noun_pool:
                        continue
                    else:
                        noun_pool.append(pos)
                        continue
                elif tag == 'NNS':  # NOUNS PLURAL
                    if pos in noun_pool:
                        continue
                    else:
                        noun_pool.append(pos)
                        continue
                elif tag == 'NNP':  # unidentified pronoun
                    if pos in pronoun_pool:
                        continue
                    else:
                        pronoun_pool.append(pos)
                        continue
                elif tag == 'JJ':  # ADJECTIVES
                    if pos in adjectives_pool:
                        continue
                    else:
                        adjectives_pool.append(pos)
                        continue
                elif tag == 'VBP':  # VERB
                    if pos in verb_pool:
                        continue
                    else:
                        verb_pool.append(pos)
                        continue
                elif tag == 'VRB':
                    if pos == "do" and self.question:
                        if pos in WP_pool:
                            continue
                        else:
                            WP_pool.append(pos)
                            continue
                    else:
                        if pos in VRB_pool:
                            continue
                        else:
                            VRB_pool.append(pos)
                            continue
                elif tag == 'VB':
                    if pos in simple_verb_pool:
                        continue
                    else:
                        simple_verb_pool.append(pos)
                        continue
                elif tag == 'VBD':
                    if pos in past_verb_pool:
                        continue
                    else:
                        past_verb_pool.append(pos)
                        continue
                elif tag == 'VBG':
                    if pos in verb_pool:
                        continue
                    else:
                        verb_pool.append(pos)
                        continue
                elif tag == 'VBZ':
                    if pos in verb_pool:
                        continue
                    else:
                        verb_pool.append(pos)
                        continue
                elif tag == 'RB':  # Example : do you STILL like me ?
                    if pos in rb_pool:
                        continue
                    else:
                        rb_pool.append(pos)
                        continue
                elif tag == 'MD':
                    if pos in MD_pool:
                        continue
                    else:
                        MD_pool.append(pos)
                        continue
                elif tag == 'WRB':
                    if pos in WRB_pool:
                        continue
                    else:
                        WRB_pool.append(pos)
                        continue
                elif tag == 'WP':
                    if pos in WP_pool:
                        continue
                    else:
                        WP_pool.append(pos)
                        continue
                else:
                    continue
        word_bank.append(pronoun_pool)
        word_bank.append(noun_pool)
        word_bank.append(verb_pool)
        word_bank.append(adjectives_pool)
        word_bank.append(WP_pool)
        word_bank.append(VRB_pool)
        word_bank.append(simple_verb_pool)
        word_bank.append(past_verb_pool)
        word_bank.append(verb_pool)
        word_bank.append(rb_pool)
        word_bank.append(MD_pool)
        word_bank.append(WRB_pool)
        return word_bank

    def apply_weights(self,word_bank,question,sentence,object_name,detail_name):
        final_word_bank = []

        print("LENGTH: " + str(len(word_bank)))
        banana_split = sentence.split(" ")
        print("BANANA : " + str(banana_split))
        print(object_name)
        print(detail_name)
        for i in range(0,10):
            if len(word_bank[i]) == 0:
                continue
            for j,word in enumerate(word_bank[i]):
                print(j)
                print(word)
                if word not in banana_split:
                    word_bank[i].pop(j)
            if i < 10:
                i += 1
        print("NEW WORD BANK : "+str(word_bank))
        sim_v, sim_s = self.find_synonyms('plan',type='noun')
        print(str(sim_v))
        print(str(sim_s))
        if question:
            #apply weightage to pronouns, verbs and question intent
            print("")
        elif not question:
            #apply weightage to nouns, verbs and question types
            print("")

        return word_bank

    def find_synonyms(self,word,type):
        syns = wordnet.synsets(str(word))
        if type == 'noun':
            params = str(word)+'.n.01'
            w1 = wordnet.synset(params)
            sim_max = 0.0
            n_max = ''
            fsim_score = 0.0
            for n in syns:
                sim_score = w1.wup_similarity(n)
                if sim_score is None:
                    break
                else:
                    fsim_score = float(sim_score)
                if fsim_score == 1.0:
                    continue
                if fsim_score > sim_max:
                    sim_max = fsim_score
                    n_max = n
            return n_max,sim_max
        elif type == 'verb':
            params = str(word)+'.v.01'
            w1 = wordnet.synset(params)
            sim_max = 0
            v_max = 0
            fsim_score = 0.0
            for v in syns:
                sim_score = w1.wup_similarity(v)
                if sim_score is None:
                    break
                else:
                    fsim_score = float(sim_score)
                if fsim_score == 1.0:
                    continue
                if fsim_score > sim_max:
                    sim_max = fsim_score
                    v_max = v
            return v_max,sim_max

    def connect_components(self):
        return self

    def component_election(self):
        return self

    def create_raw_response(self):
        return self

    def fine_tune_response(self):
        return self