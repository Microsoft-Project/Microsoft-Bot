from flask import Flask, request
from flask_cors import CORS, cross_origin
import make_prediction

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# API
# 1. Post request for label prediction
# 2. Get word embeddings
# 3. Get processed text(data)
# 4. Get data info, returns no of data points used for training and schema of the
# 	 training data.


@app.route('/api/prediction', methods=['POST'])
@cross_origin()
def root():
    # data that we get from the post request
    data = request.get_json(force=True)
    data = data['title'] + ' ' + data['body']
    processed_data, prediction = make_prediction.make_prediction(data)
    print("-------")
    print(prediction)
    return {'predictedLabel': prediction[0], "processedData": processed_data}


@app.route('/embeddings')
def embeddings():
    name = request.args.get("name", "World")
    print(request.args)
    result = {'name': name, 'what': 'World'}
    return result



@app.route('/data_points')
def data_points():
    name = request.args.get("name", "World")
    result = {'name': name, 'what': 'World'}
    return result

# with app.test_request_context():
#     url_for('static', filename='a.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')