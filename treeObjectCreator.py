import shutil
import os

class TreeObjectCreator:
    object_name = ""
    d_name = ""
    d_type = ""
    d_raw_text = ""
    p_score = 0
    fam_score = 0
    unknown_score = 0
    branch_level = 0
    semantic_score = 0
    line_count =[]
    def __init__(self,object_name,branch_level,d_name,d_type,d_raw_text,p_score,fam_score,unknown_score,semantic_score):
        self.object_name = object_name
        self.branch_level = branch_level
        self.d_name = d_name
        self.d_type = d_type
        self.d_raw_text = d_raw_text
        self.p_score = p_score
        self.fam_score = fam_score
        self.unknown_score = unknown_score
        self.semantic_score = semantic_score
        #object initiation

    def update_object_node(self,object_name,branch_level,detail_raw_text,personal_score,fam_score,pointList,unknown_score,semantic_score):
        t = open("localTree.txt","r")
        #update the local tree object by object name (UNIQUE)
        all_objects_raw_text = t.read().split('\n\n')
        count = 0
        for objectEntry in all_objects_raw_text:
            count+=1
            print("OBJECT ENTRY " + str(count) + " : \n" + objectEntry +'\n')
        return self

    def add_object_node(self,object_name, branch_level, d_name, d_type, d_raw_text, p_score, understand_score, unknown_score,semantic_score):
        new_object = ""
        if os.path.getsize('localTree.txt') == 0:
            print("1")
            new_object = 'ObjectName:' + str(object_name) + '\n\t<detail>BranchLevel:'+str(branch_level)+',DetailName:'+d_name+',DetailType:'+d_type+',DetailRawText:'+d_raw_text+',PersonalScore:'+str(p_score)+',UnderstandScore:'+str(understand_score)+',UnknownScore:'+str(unknown_score)+',SemanticScore:'+str(semantic_score)+'</detail>'
        else:
            print("2")
            new_object = '\n\n'+'ObjectName:' + str(object_name) + '\n\t<detail>BranchLevel:'+str(branch_level)+',DetailName:'+d_name+',DetailType:'+d_type+',DetailRawText:'+d_raw_text+',PersonalScore:'+str(p_score)+',UnderstandScore:'+str(understand_score)+',UnknownScore:'+str(unknown_score)+',SemanticScore:'+str(semantic_score)+'</detail>'
        with open("localTree.txt","r") as r:
            for i,line in enumerate(r):
                if i == 0 and not line.strip():
                    print("3")
                    new_object = '\n\nObjectName:' + str(object_name) + '\n\t<detail>BranchLevel:'+str(branch_level)+',DetailName:'+d_name+',DetailType:'+d_type+',DetailRawText:'+d_raw_text+',PersonalScore:'+str(p_score)+',UnderstandScore:'+str(understand_score)+',UnknownScore:'+str(unknown_score)+',SemanticScore:'+str(semantic_score)+'</detail>'
        with open("localTree.txt","a") as t:
            t.write(new_object)
            t.close()

    def check_object_node(self,object_name):
        objfound = False
        with open("localTree.txt","r") as t:
            target = "ObjectName:" + object_name
            print("Opened the local tree")
            lineNum = 0
            for line in t:
                lineNum += 1
                if target in str(line):
                    print("FOUND THE TARGET: " + line + " LINE NUMBER: " + str(lineNum))
                    objfound = True
                    break
                else:
                    objfound = False
                    continue
        t.close()
        print("objfound is " + str(objfound))
        if lineNum != 0:
            lineNum += 1
        return lineNum,objfound

    def check_object_details(self,objLineNum):
        detailLineNum = 0 #the last detail line number of that specific object - more efficient than re-iterating
        count = 0
        found = False
        with open("localTree.txt","r") as t:
            print("checking for object details...")
            lastDetail = 1
            for i,line in enumerate(t):
                if line.strip() and found and i != objLineNum - 2:
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
        return count, detailLineNum

    def add_detail_node(self,detailLineNum,branch_level,detail_name,detail_type,sentence,personal_score,fam_score,unknown_score,semantic_score):
        temp = open('temp','w')
        with open("localTree.txt","r") as t:
            all_lines = t.readlines()
            max = 0
            for i, line in enumerate(all_lines):
                max = i
            print(max)
            print("appending details.........")
            attachment = '\t<detail>BranchLevel:' + str(
                branch_level) + ',DetailName:' + detail_name + ',DetailType:' + detail_type + ',DetailRawText:' + sentence + ',PersonalScore:' + str(
                personal_score) + ',UnderstandScore:' + str(fam_score) + ',UnknownScore:' + str(
                unknown_score) + ',SemanticScore:' + str(semantic_score)+"</detail>"
            print(attachment)

            for i,line in enumerate(all_lines):
                print("LINE " + str(i+1))
                if i != detailLineNum - 1:
                    print("doing A")
                    temp.write(line)
                if i == detailLineNum - 1 and i == max:
                    line_new = line+'\n'+attachment
                    print("doing B")
                    temp.write(line_new)
                elif i == detailLineNum - 1 and i != max:
                    print("doing C " + line)
                    fresh_line = line.strip()
                    fresh_line = "\t" + fresh_line
                    temp.write(fresh_line)
                elif i == detailLineNum and i != max and not line.strip():
                    print("doing D " + line)
                    fresh_line = line.strip()
                    fresh_line = attachment+ '\n\n'
                    temp.write(fresh_line)
        temp.close()
        shutil.move('temp','localTree.txt')
        open("temp",'w').close()
        t.close()
        return self

    def show_object_nodes(self):
        t = open("localTree.txt","r")
        #update the local tree object by object name (UNIQUE)
        all_objects_raw_text = t.read().split('\n\n')
        count = 0
        for objectEntry in all_objects_raw_text:
            count+=1
            print("OBJECT ENTRY " + str(count) + " : \n" + objectEntry +'\n')
        return self
