from flask import Flask,redirect,url_for,request,jsonify
app = Flask(__name__)

@app.route('/remember',methods=['GET'])
def remember_server_memory():
    noun_pool = request.args.getlist('noun_pool')
    server_memory = []
    with open('serverTree.txt','r') as s:
        all_lines = s.readlines()
        for i, line in enumerate(all_lines):
            if "ObjectName:" in line:
                continue
            elif line == "":
                continue
            else:
                component = rawTextFinder(4, (line.strip()).split(","))
                for word in noun_pool:
                    if word == "":
                        continue
                    elif word.lower() in component.lower():
                        server_memory.append(component)
                        break
    return str(server_memory)

def rawTextFinder(componentNumber,line):
    component = ""
    for i, componentRaw in enumerate(line):
        if i+1 == componentNumber:
            component = (componentRaw.split(":"))[1]
    return str(component)

if __name__ == '__main__':
    app.run()