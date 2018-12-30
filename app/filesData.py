from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
from .Transformio import Transformio
import json
import ast
import imp


# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Select the database
db = client.DjangoTest
# Select the collection
collection = db.Files

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'status': '200',
        'message': 'Atlantis Files API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/api/files", methods=['POST'])
def create_file():
    """
       Function to create new FILES.
       """
    file = request.files["name"]
    image = Transformio(file)
    # image.showFormat()
    image.tryCompress()
    try:
        if "name" not in request.files:
            return "No name key in request.files"
        else:
        # Create new files
            # file = request.files["name"]
            try:
                

                body = {"name": file.filename, 
                "createdAt": request.form["createdAt"],
                "status": request.form["status"]
                }
                print(body)
            except:
            # Bad request as request body is not available
            # Add message for debugging purpose
                return "", 400

            record_created = collection.insert(body)

            # Prepare the response
            if isinstance(record_created, list):
                # Return list of Id of the newly created item
                return jsonify([str(v) for v in record_created]), 201
            else:
                # Return Id of the newly created item
                return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500

@app.route("/api/test", methods=["POST"])
def upload_file():

	# A
    if "name" not in request.files:
        return "No name key in request.files"
    else:

        return "Ok"

	# B
    file    = request.files["name"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

@app.route("/api/files", methods=['GET'])
def fetch_files():
    """
       Function to fetch the files.
       """
    try:
        # Return all the records as query string parameters are not available
        if collection.find().count() > 0:
                # Prepare response if the users are found
            return dumps(collection.find(),)
        else:
            # Return empty array if no users are found
            return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/files/<file_id>", methods=['POST'])
def update_file(file_id):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the user
        records_updated = collection.update_one({"_id": int(file_id)}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/files/<file_id>", methods=['DELETE'])
def remove_file(file_id):
    """
       Function to remove the file.
       """
    try:
        # Delete the user
        delete_user = collection.delete_one({"-id": int(file_id)})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp