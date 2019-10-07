from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def home():
   return render_template('shoppingmall.html')

@app.route('/order', methods=['POST'])
def order_post():
   name_receive = request.form['name_give']
   count_receive = request.form['count_give']
   address_receive = request.form['address_give']
   phone_receive = request.form['phone_give']
   item_receive = request.form['item_give']

   order = {
      'name': name_receive,
      'count': count_receive,
      'address': address_receive,
      'phone': phone_receive,
      'item': item_receive,
   }

   db.orders.insert(order)

   return jsonify({'result': 'success'})

@app.route('/order', methods=['GET'])
def order_get():
   item_receive = request.args.get('item_give')
   orderlist = list(db.orders.find({'item': item_receive}, {'_id': 0}))
   return jsonify({'result': 'success', 'orders': orderlist})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)