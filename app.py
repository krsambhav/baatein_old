from flask import Flask, request
from flask.templating import render_template
from flask_socketio import SocketIO
from translate import Translator
import socketio

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    return render_template('chat.html')


def messageReceived(methods=['POST']):
    print('message was received!!!')


@socketio.on('my event')
def translate(data, methods=['POST']):
    username = str(data['username'])
    msg = str(data['msg'])
    sender_lang = str(data['lang'])
    print('this is my event socket')
    socketio.emit('my response', [
                  username, msg, sender_lang], broadcast=True, include_self=False, callback=messageReceived)



@socketio.on('connected')
def printusername():
    print('Printing ID')
    print(request.sid)
    sid = request.sid
    print('Emitting')
    socketio.emit('my sid', sid, room=sid)
    


@socketio.on('translate_self')
def translate_self(data, methods=['POST']):
    print('this is translate self')
    print(data)
    sid = data['sid']
    init_msg = data['msg']
    sender_lang = data['sender_lang']
    language = data['lang']
    user = data['recvd_username']
    final_msg = Translator(
        from_lang=sender_lang, to_lang=language).translate(init_msg)
    print(final_msg)
    print(sid)
    fdata = {sid, final_msg}
    socketio.emit('final msg', [sid, user, final_msg])


if __name__ == '__main__':
    socketio.run(app, debug=True)
