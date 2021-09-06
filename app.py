from flask import Flask, render_template, Response, request, redirect
import service

app = Flask(__name__)

@app.route('/')
def current_bulletin():
    return redirect(service.get_bulletin_url(), code=302)

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
