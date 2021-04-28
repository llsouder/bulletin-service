from service import getLatestBulletin
from flask import Flask, render_template, Response, request, redirect
from datetime import datetime

last_update = datetime.now()

last_update_string = last_update.strftime("%H:%M:%S")
print("Current Time =", last_update_string)

app = Flask(__name__)

@app.route('/')
def current_bulletin():
    return redirect(getLatestBulletin(), code=302)

@app.route('/api/web-receiver', methods=['POST'])
def respond():
    valicationToken = request.args.get("validationToken")
    if valicationToken is not None:
        print("sending back validation.")
        return valicationToken
    request_value = request.json["value"][0]
    print("post: ", request_value["resource"], request_value["changeType"])
    return ""

if __name__=="__main__":
      app.run(debug=True)
