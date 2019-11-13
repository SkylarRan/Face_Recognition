from flask import Flask, make_response, request, jsonify
import uuid
from db import Blacklist, Record, database
from upload import upload_blacklist_image
from videoThread import VideoThread, stop_thread
from playhouse.shortcuts import model_to_dict

app = Flask(__name__, static_url_path='/api/v1.0')
url_appfix = "/api/v1.0"


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


def set_response(dic):
    response = make_response(jsonify(dic))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route(url_appfix + '/test', methods=['GET'])
def test():
    response = set_response({'status': True})
    return response


@app.route(url_appfix + '/records', methods=['GET', 'OPTIONS'])
def records():
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    try:
        total = Record.select().count()
        records = (Record.select().order_by(Record.recognizedAt)).offset(int(offset)).limit(int(limit))
        data = []
        for r in records:
            data.append(model_to_dict(r))
        res = {'status': True, 'data': data, 'total': total}
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}
    finally:
        response = set_response(res)
        return response


@app.route(url_appfix + '/blacklists', methods=['GET', 'OPTIONS'])
def blacklists():
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    try:
        total = Blacklist.select().count()
        blacklists = (Blacklist.select().order_by(Blacklist.name)).offset(int(offset)).limit(int(limit))
        data = []
        for b in blacklists:
            data.append(model_to_dict(b))
        res = {'status': True, 'data': data, 'total': total}
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}
    finally:
        response = set_response(res)
        return response


@app.route(url_appfix + '/blacklists/<id>', methods=['GET'])
def get(id):
    try:
        b = Blacklist.get(Blacklist.id == id)
        data = model_to_dict(b)
        res = {'status': True, 'data': data}
    except Exception as e:
        print(e)
        res = {'status': False, 'message': "No data found."}
    finally:
        response = set_response(res)
        return response


@app.route(url_appfix + '/blacklist/save', methods=['POST'])
def save_blacklist():
    id = request.form.get("id")
    name = request.form.get("name")
    image = request.files.get("image")
    memo = request.form.get("memo")

    if id == '':
        if name is None or image is None:
            response = set_response({'status': False, 'message': 'Parameter error'})
            return response
        res = add_blacklist(name, image, memo)
    else:
        res = edit_blacklist(id, name, image, memo)

    response = set_response(res)
    return response


@app.route(url_appfix + '/blacklist/delete', methods=['POST'])
def delete_blacklist():
    id = request.form.get("id")
    if id is None:
        response = set_response({'status': False, 'message': 'Parameter error'})
        return response

    try:
        b = Blacklist.get(Blacklist.id == id)
        b.delete_instance()
        res = {'status': True}
        print("delete success:" + id)
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}

    response = set_response(res)
    return response


def add_blacklist(name, image, memo):
    try:
        path = upload_blacklist_image(image)
        Blacklist.create(id=uuid.uuid1(), name=name, memo=memo, image=path)
        res = {'status': True}
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}

    return res


def edit_blacklist(id, name, image, memo):
    try:
        if image is None:
            query = (Blacklist
                     .update({Blacklist.name: name, Blacklist.memo: memo})
                     .where(Blacklist.id == id))
        else:
            path = upload_blacklist_image(image)
            query = (Blacklist
                     .update({Blacklist.name: name, Blacklist.memo: memo, Blacklist.image: path})
                     .where(Blacklist.id == id))

        query.execute(database)
        res = {'status': True}
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}

    return res


@app.route(url_appfix + '/recognize/start', methods=['POST', 'OPTIONS'])
def start_recognize():
    res = {'status': True}
    if request.method != 'OPTIONS':
        rtmp = request.json.get("rtmp") 
        name = request.json.get("name") 
        location = request.json.get("location") 
        record_interval = request.json.get("interval") 
        if rtmp is None or name is None or location is None or record_interval is None:
            response = set_response({'status': False, 'message': 'Parameter error'})
            return response

        t = VideoThread(rtmp, name, location, record_interval)
        t.start()
        res = {'status': True, 'data':[t.ident]}
    response = set_response(res)
    return response


@app.route(url_appfix + '/recognize/stop', methods=['POST', 'OPTIONS'])
def stop_recognize():
    res = {'status': True}
    if request.method != 'OPTIONS':
        tids = request.json.get("tids") 
        try:
            stop_thread(tids[0])
        except Exception as e:
            res = {'status': False, 'message': str(e)}
        print("stoped")
    response = set_response(res)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
