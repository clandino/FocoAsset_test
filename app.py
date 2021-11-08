from myFlask import create_app

app = create_app(1)

@app.route('/')
def hello():
    return "Hello World!"