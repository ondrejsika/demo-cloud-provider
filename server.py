import os
import hashlib
import json
import dataset
from flask import Flask, request, Response


app = Flask(__name__)
db = dataset.connect(os.environ.get("DATABASE_URL", ""))


@app.route("/v1/box/", methods=["GET"])
def get_boxes():
    return json.dumps(list(db["boxes"].find()))


@app.route("/v1/box/", methods=["POST"])
def create_box():
    box_id = db["boxes"].insert({"name": request.json["name"]})
    return json.dumps({"box_id": box_id})


@app.route("/v1/box/<int:box_id>/", methods=["GET"])
def get_box(box_id):
    return json.dumps(dict(db["boxes"].find_one(id=box_id)))


@app.route("/v1/box/<int:box_id>/", methods=["PUT"])
def update_box(box_id):
    db["boxes"].update({"name": request.json["name"], "id": box_id}, ['id'])
    return json.dumps({"ok": True})


@app.route("/v1/box/<int:box_id>/", methods=["DELETE"])
def delete_box(box_id):
    db["boxes"].delete(id=box_id)
    return json.dumps({"ok": True})


@app.route("/v1/box/<int:box_id>/text/", methods=["GET"])
def get_texts(box_id):
    return json.dumps(list(db["texts"].find(box_id=box_id)))


@app.route("/v1/box/<int:box_id>/text/", methods=["POST"])
def create_text(box_id):
    text_id = db["texts"].insert({"box_id": box_id, "text": request.json["text"]})
    return json.dumps({"text_id": text_id})


@app.route("/v1/box/<int:box_id>/text/<int:text_id>/", methods=["GET"])
def get_text(box_id, text_id):
    return json.dumps(dict(db["texts"].find_one(box_id=box_id, id=text_id)))


@app.route("/v1/box/<int:box_id>/text/<int:text_id>/", methods=["PUT"])
def update_text(box_id, text_id):
    db["texts"].update({"text": request.json["text"], "id": text_id, "box_id": box_id}, ['id', "box_id"])
    return json.dumps({"ok": True})


@app.route("/v1/box/<int:box_id>/text/<int:text_id>/", methods=["DELETE"])
def delete_text(box_id, text_id):
    db["boxes"].delete(box_id=box_id, id=text_id)
    return json.dumps({"ok": True})


@app.route("/", methods=["GET"])
def index():
    out = []
    box_dict = {}
    for box in db["boxes"].find():
        out.append("Box: %s %s\n" % (box['id'], box['name']))
        for text in db["texts"].find(box_id=box["id"]):
            out.append("    Text: %s %s\n" % (text["id"], text["text"]))
        out.append("\n")
    return Response("".join(out), content_type="text/plain")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="80", threaded=False, processes=1)
