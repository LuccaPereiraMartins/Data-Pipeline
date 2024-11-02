from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

# use flask server for api
# initialise flask application
app = Flask(__name__)

# retrieve data from processed folder
data = pd.read_csv('processed/test.csv', index_col='ticker')

# create simple route, use decorator to make accessible
# define path to access (after the /)
@app.route('/')
def home():
    return 'HOME PAGE'


# create some more methods
# GET request data from a specific resource
# POST create a resource
# PUT update a resource
# DELETE delete a resource


# create a method to return all the data as a dictionary
@app.route('/all', methods=['GET'])
def return_all():
    # return the dictionary of specified description with a 200 status code if passed
    return jsonify(data.to_dict()), 200

# create a method to return all the data as a downloadable csv
@app.route('/download_all', methods=['GET'])
def download_all():
    # Define the absolute or relative path to the file
    path = os.path.join(os.getcwd(), 'processed', 'test.csv')

    # Check if the file exists
    if not os.path.isfile(path):
        return "File not found", 404

    return send_file(path, as_attachment=True), 200

# create a method to return the row data for a specified description
@app.route('/specific-data/<description>', methods=['GET'])
def get_specific(description):
    data_specific = data.loc[description,:]
    # return the dictionary of specified description with a 200 status code if passed
    return jsonify(data_specific.to_dict()), 200

# TODO fix how to return the index too, orient='index' argument doesn't seem to work


# TODO attempt at creating a get post method
@app.route('/append-description/<description>', methods=['POST'])
def append_description(description):
    # suppose the specific description had a valid row of data associated with it
    row = None
    data.append(row)
    return jsonify(data.to_dict())


# Example URL after running script
# http://127.0.0.1:5000/specific-data/TESLA%20INC



# basic line to run flask server
if __name__ == '__main__':
    app.run(debug=True)
