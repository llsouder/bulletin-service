from service import getLatestBulletin
from flask import Flask, render_template, Response, request


app = Flask(__name__)

@app.route('/')
def current_bulletin():
    return render_template('index.html', webUrl=getLatestBulletin())

@app.route('/api/web-receiver', methods=['POST'])
def respond():
    valicationToken = request.args.get("validationToken")
    if valicationToken is not None:
        print("sending back validation.")
        return valicationToken
    print(request.json)
    return ""


if __name__=="__main__":
      app.run(debug=True)
