class TreeObjectCreator :
    object_name = ""
    d_name = ""
    d_type = ""
    d_raw_text = ""
    p_score = 0
    understand_score = 0
    unknown_score = 0
    branch_level = 0
    semantic_score = 0

    def __init__(self,object_name,branch_level,d_name,d_type,d_raw_text,p_score,understand_score,unknown_score,semantic_score):
        self.object_name = object_name
        self.branch_level = branch_level
        self.d_name = d_name
        self.d_type = d_type
        self.d_raw_text = d_raw_text
        self.p_score = p_score
        self.understand_score = understand_score
        self.unknown_score = unknown_score
        self.semantic_score = semantic_score
        #object initiation

    def update_object_node(self,object_name,branch_level,detail_raw_text,personal_score,understand_score,pointList,unknown_score,semantic_score):
        t = open("localTree.txt","r")
        #update the local tree object by object name (UNIQUE)
        all_objects_raw_text = t.read().split('\n\n')
        count = 0
        for objectEntry in all_objects_raw_text:
            count+=1
            print("OBJECT ENTRY " + str(count) + " : \n" + objectEntry +'\n')
        return self

    def add_object_node(self,object_name, branch_level, d_name, d_type, d_raw_text, p_score, understand_score, unknown_score,semantic_score):
        with open("localTree.txt","a") as t:
            t.write('\n\nObjectName:' + str(object_name) + '\nBranchLevel:'+str(branch_level)+',DetailName:'+d_name+',DetailType:'+d_type+',DetailRawText:'+d_raw_text+',PersonalScore:'+str(p_score)+',UnderstandScore:'+str(understand_score)+',UnknownScore:'+str(unknown_score)+',SemanticScore:'+str(semantic_score))
            t.close()

    def show_object_nodes(self):
        t = open("localTree.txt","r")
        #update the local tree object by object name (UNIQUE)
        all_objects_raw_text = t.read().split('\n\n')
        count = 0
        for objectEntry in all_objects_raw_text:
            count+=1
            print("OBJECT ENTRY " + str(count) + " : \n" + objectEntry +'\n')
        return self
