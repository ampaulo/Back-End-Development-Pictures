from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id): 
    if data:
        for x in data:
            if x["id"] == id:
                return jsonify(x), 200

    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    data_tmp = json.loads(request.data)
    if data:
        for x in data:
            if x["id"] == data_tmp["id"]:
                return jsonify(Message=f"picture with id {data_tmp['id']} already present"), 302

        data.append(data_tmp)
        return {"id": data_tmp["id"]}, 201

    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    data_tmp = json.loads(request.data)
    if data:
        for x in range(len(data)):
            if data[x]["id"] == data_tmp["id"]:
                data[x] = data_tmp
                return jsonify(Message=f"OK"), 200

    return {"message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for x in range(len(data)):
            if data[x]["id"] == id:
                data.pop(x)
                return jsonify(Message=f"OK"), 204

    return {"message": "Picture not found"}, 404
