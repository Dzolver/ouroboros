#currently, the wish log is set to package every 5 inputs
class wishLogCreator:
    object_name = ""
    detail_name = ""
    detail_line_num = 0
    raw_text = ""
    wish = ""

    def __init__(self,object_name,detail_name,detail_line_num,raw_text):
        self.object_name = object_name
        self.detail_name = detail_name
        self.detail_line_num = detail_line_num
        self.raw_text = raw_text

    def update_wish_log(self,object_name,detail_name,detail_line_num,raw_text):
        with open('wishLog.txt','a') as w:
            wish = '{"object_name":"'+object_name+'","detail_name":'+detail_name+',"detail_line_num":'+str(detail_line_num)+',"raw_text:"'+raw_text+'}'+'\n'
            w.write(wish)
            w.close()
        fw = open('logs/wishLog.txt','a')
        fw.write(wish)
        fw.close()
        return wish