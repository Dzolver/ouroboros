from flask import Flask
import time
app = Flask(__name__)
@app.route("/")
def GrantWish():
    i = 0
    i += 1
    time.sleep(2)
    return i

if __name__ == "__main__":
    app.run()