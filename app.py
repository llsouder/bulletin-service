from flask import Flask, render_template, Response, request, redirect

app = Flask(__name__)

@app.route('/')
def current_bulletin():
    return redirect("https://www.vbchammonton.org/uploads/3/7/1/8/3718617/july_25th_bulletin.pdf", code=302)

if __name__=="__main__":
      app.run()
