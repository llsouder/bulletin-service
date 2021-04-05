from service import tooCool, getLatestBulletin
from flask import Flask




app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/x')
def test_route():
    return  getLatestBulletin()



if __name__=="__main__":
      app.run()
