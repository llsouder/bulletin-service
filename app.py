from service import tooCool, getLatestBulletin
from flask import Flask, render_template




app = Flask(__name__)

@app.route('/')
def current_bulletin():
    return render_template('index.html', webUrl=getLatestBulletin())

@app.route('/x')
def test_route():
    return  getLatestBulletin()



if __name__=="__main__":
      app.run()
