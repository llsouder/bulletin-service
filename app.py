from flask import Flask, render_template, Response, request, redirect
import service

app = Flask(__name__)


@app.route('/')
def current_bulletin():
    return redirect(service.get_bulletin_url(), code=302)

@app.route('/test-bull')
def test():
    return redirect(service.get_bulletin_url(), code=302)

@app.route('/see-bull')
def seeUrl():
    return service.show_login()
    #return "testing 1 2 3."

if __name__=="__main__":
      app.run()
