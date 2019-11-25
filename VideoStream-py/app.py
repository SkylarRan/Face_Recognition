from flask import Flask,request,abort,make_response,jsonify
from domain import Result
from webapi import Camera_Api
app = Flask(__name__)
api=Camera_Api()

@app.route('/api/v1.0/test', methods=['Get', 'OPTIONS'])
def api_test():
    result= Result()
    result.status="Success"
    result.data=[]
    result.message=""
    return api_response(result.result2dict())

@app.route('/api/v1.0/cameras', methods=['Get', 'OPTIONS'])
def cameralist():
    result=api.getlist()
    return api_response(result)

@app.route('/api/v1.0/cameras/<int:camera_id>', methods=['Get', 'OPTIONS'])
def camera(camera_id):
    result=api.get(camera_id)
    return api_response(result)

@app.route('/api/v1.0/cameras/add', methods=['Post', 'OPTIONS'])
def cameraAdd():
    if not request.form:
        abort(400)
    result=api.add(request.form)
    return api_response(result)

@app.route('/api/v1.0/cameras/edit', methods=['Post', 'OPTIONS'])
def cameraEdit():
    if not request.form:
        abort(400)
    result=api.edit(request.form)
    return api_response(result)


@app.route('/api/v1.0/cameras/delete', methods=['Post', 'OPTIONS'])
def cameraDelete():
    if not request.form:
        abort(400)
    result=api.delete(request.form)
    return api_response(result)

@app.route('/api/v1.0/streams', methods=['Get', 'OPTIONS'])
def streams():
    result=api.getstreamlist()
    return api_response(result)

def api_response(dict):
    response = make_response(jsonify(dict))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

api.startallstream()
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000,use_reloader=False)