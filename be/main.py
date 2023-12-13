from pymongo import MongoClient
from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
from common import hash_password, verify_password
from vectordatabase import qa

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")
client = MongoClient("localhost", 27017)
db = client['python-demo']

user_entity = db.users
message_entity = db.messages
chat_entity = db.chats

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    exist_user = user_entity.find_one({ "username": data.get('username')})
    if exist_user:
        return jsonify({ "status": 301, "message": "user existing" })
    hashed_password = hash_password(data.get('password').encode('utf-8'))
    new_user = {
        "username": data.get('username'),
        "password": hashed_password.decode('utf-8') 
    }
    user_entity.insert_one(new_user)
    return jsonify({ "status": 200 })

@app.route('/login', methods=['GET'])
def login():
    data = request.args
    exist_user = user_entity.find_one({ "username": data.get('username')})
    if not exist_user:
        return jsonify({ "status": 404, "message": "user not found" })
    verifyed_password = verify_password(data.get('password').encode('utf-8'), exist_user.get('password').encode('utf-8'))
    if not verifyed_password:
        return jsonify({ "status": 404, "message": "user not found" })
    exist_user['_id'] = str(exist_user['_id'])
    return jsonify({ "status": 200, "data": exist_user })

@app.route('/new_chat', methods=['POST'])
def new_chat():
    data = request.get_json()
    chat = chat_entity.insert_one(data)
    _new = {
        "_id": str(chat.inserted_id),
        "name": data.get('name'),
        "user_id": data.get('user_id')
    }
    return jsonify({ "status": 200, "data": _new })

@app.route('/chats', methods=['GET'])
def chats():
    data = request.args
    _chats = list(chat_entity.find({ "user_id": data.get('user_id') }))
    for i in _chats:
        i['_id'] = str(i['_id'])
    return jsonify({ "status": 200, "data": list(_chats)})

@socketio.on('get_messages')
def get_messages(data):
    _messages = message_entity.find({ "in": data['in'] })
    _messages = list(_messages)
    for i in _messages:
        i['_id'] = str(i['_id'])
    emit('get_messages', {"data": _messages, "in": data['in']})

@socketio.on('new_message')
def new_message(data):
    message = message_entity.insert_one(data)
    _id = str(message.inserted_id)
    emit('new_message', { "_id": _id, "user_id": data['user_id'], "content": data['content'], "type": data['type'], "in": data['in']})
    answer = qa.run(data['content'])
    print(answer)
    ai_message = message_entity.insert_one({
        "user_id": data['user_id'],
        "content": answer,
        "type": 'ai',
        "in": data['in']
    })
    _id_ai = str(ai_message.inserted_id)
    emit('new_message', { "_id": _id_ai, "user_id": data['user_id'], "content": answer, "type": 'ai', "in": data['in']})

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect_success", {"data": f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    # emit("data", {'data': data, 'id': request.sid}, broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    # emit("disconnect", f"user {request.sid} disconnected", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
