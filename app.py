from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.mysite  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/chat', methods=['POST'])
def chat_send():
	# 1. 클라이언트가 준 id, content 가져오기.
    mid = request.form['mid']
    content = request.form['content']

	# 2. DB에 정보 삽입하기
    newChat = {
        'mid'     : mid,
        'content' : content
    }

    db.chat.insert_one(newChat)

	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({
        'result': 'success'
    })


@app.route('/chat', methods=['GET'])
def chat_read():
    chat = list(db.chat.find({}, {'_id': 0}))
    return jsonify({
        'result': 'success',
        'chat': chat
    })

@app.route('/login', methods=['POST'])
def chat_login():
    name = request.form['name']
    pwd = request.form['pwd']

    login = {
        'name' : name,
        'pwd' : pwd
    }

    db.login.insert_one(login)

    return jsonify({
        'result': 'success'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

