from flask import Flask
from button import load_primary_video
app = Flask(__name__) 

@app.route('/')
def index():
    load_primary_video()
    return 'I miss you everyday Ira.' 

if __name__ == "__main__":
    app.run()