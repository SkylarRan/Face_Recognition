from flask import Flask, make_response, request, jsonify
import uuid
from db import Blacklist, Record, database
from imgUtil import upload_blacklist_image, remove_image
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
        records = (Record.select().order_by(Record.recognizedAt.desc())).offset(int(offset)).limit(int(limit))
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
        remove_image("blacklist",id)
        res = {'status': True}
        print("delete success:" + id)
    except Exception as e:
        print(e)
        res = {'status': False, 'message': str(e)}

    response = set_response(res)
    return response


def add_blacklist(name, image, memo):
    try:
        id=str(uuid.uuid1())
        path = upload_blacklist_image(image, id)
        Blacklist.create(id=id, name=name, memo=memo, image=path)
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
            path = upload_blacklist_image(image, id)
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
        record_interval = request.json.get("interval") 
        streams = request.json.get("streams")
        if streams and len(streams) > 0:
            pids = []
            for s in streams:
                p = VideoThread(s['id'], s['rtmp'], s['name'], s['location'], record_interval)
                p.start()
                pids.append(p.ident)
            res = {'status': True, 'data': pids}
        else:
            res = {'status': False, 'message': 'No useful stream'}
    response = set_response(res)
    return response


@app.route(url_appfix + '/recognize/stop', methods=['POST', 'OPTIONS'])
def stop_recognize():
    res = {'status': True}
    if request.method != 'OPTIONS':
        tids = request.json.get("tids")
        if not tids:
            res = {'status': False, 'message': 'invalid Paramters.'}
        else:
            try:
                for i in range(len(tids)):
                    stop_thread(tids[i])
            except Exception as e:
                res = {'status': False, 'message': str(e)}
            print("stoped")
    response = set_response(res)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
