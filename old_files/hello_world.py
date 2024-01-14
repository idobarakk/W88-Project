from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return open('hello_world.html').read()

@app.route('/submit', methods=['POST'])
def submit():
    input_data = request.form['inputData']
    
    # Handle the input data as needed (e.g., save to a database, process, etc.)
    
    return "Data received: {}".format(input_data)

if __name__ == '__main__':
    app.run(debug=True)
