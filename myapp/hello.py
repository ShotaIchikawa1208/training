from flask import Flask, request, render_template
from flask import session, redirect, url_for
from datetime import timedelta
import json
import validation
import db_connect

app = Flask(__name__)

# sessionに格納する情報のため必ず必要
app.secret_key = 'abcdefghijklmn'
# ３分操作がなければsession破棄するよう設定
app.permanent_session_lifetime = timedelta(minutes=3)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['e-mail']
    password = request.form['password']
    db = db_connect.DBconnect()
    user_id = db.login_check(email, password)

    if user_id:
        message = 'ログイン成功'
        user, user_shikaku_list = db.search_user(user_id)
        session['user_id'] = user['user_id']
        session['user_name'] = user['name']
        name = session['user_name']
        return render_template('user_page.html', user=user,
                               user_shikaku_list=user_shikaku_list,
                               message=message, name=name)
    else:
        message = 'ログイン失敗'
        return render_template('index.html', message=message)


@app.route('/account_register')
def form():
    return render_template('account_register.html')


# ユーザー一覧
@app.route('/users_table')
def show_users_table():
    db = db_connect.DBconnect()
    users_info_list, users_shikaku_list = db.get_users()

    return render_template('users_table.html', users=users_info_list,
                           users_shikaku_list=users_shikaku_list)


# ユーザーページ
@app.route('/user/<int:id>')
def user_page(id):
    print('user_page関数内')
    print(type(id))
    db = db_connect.DBconnect()
    user, user_shikaku_list = db.search_user(id)

    name = session['user_name']
    return render_template('user_page.html', user=user,
                           user_shikaku_list=user_shikaku_list, name=name)


# アカウント登録
@app.route('/new', methods=['POST'])
def account_register():
    # users表に登録するデータ
    new_user = {
        "name": request.form['name'],
        "mail": request.form['e-mail'],
        "password": request.form['password'],
    }

    # user_infoに登録するデータ
    new_user_info = {
        "name_kana": request.form['name_kana'],
        "gender": request.form['gender'],
        "yubin": request.form['yubin'],
        "ken_code": request.form['ken_code'],
        "shiku": request.form['shiku'],
        "jyusyo": request.form['jyushyo'],
        "tel": request.form['tel'],
    }

    # user_sikakuに登録するデータ
    user_sikaku_list = request.form.getlist('sikaku')

    db = db_connect.DBconnect()
    message = db.account_register(new_user, new_user_info, user_sikaku_list)
    return render_template('index.html', message=message)


# メールアドレスに重複がないか確認（非同期）
@app.route('/mail_check', methods=['POST'])
def mail_check():
    mail = request.form.get('e-mail')
    print(mail)
    judg = validation.check_mail(mail)
    print(type(judg))
    print(judg)
    if not judg:
        print('NO')
        return 'NO'
    else:
        return 'OK'


# 入力郵便番号から住所取得
@app.route('/search_address', methods={'POST'})
def search_address():
    # yubin = request.form.get('yubin')

    data = request.json
    yubin = data['yubin']

    result_dict = validation.search_address(yubin)

    # print(result_dict)
    result_json = json.dumps(result_dict, ensure_ascii=False, indent=2)
    # print('json' + result_json)
    return result_json


# アカウント更新
@app.route('/update')
# session['user_id']があるか確認して内容記入ページに飛ばす
def go_edit():
    if 'user_id' in session:
        user_id = session['user_id']
        print(type(user_id))
        user_name = session['user_name']
        return render_template('edit_user_info.html', user_id=user_id,
                               user_name=user_name)
    else:
        message = 'ログインしなおしてください'
        return render_template('index.html', message=message)


@app.route('/update/<int:user_id>', methods=['POST'])
def account_update(user_id):
    # users表に登録するデータ
    new_user_info = {
        "name": request.form['name'],
        "mail": request.form['e-mail'],
        "password": request.form['password'],
    }

    # user_infoに登録するデータ
    new_user_subinfo = {
        "name_kana": request.form['name_kana'],
        "gender": request.form['gender'],
        "yubin": request.form['yubin'],
        "ken_code": request.form['ken_code'],
        "shiku": request.form['shiku'],
        "jyusyo": request.form['jyushyo'],
        "tel": request.form['tel'],
    }

    # user_sikakuに登録するデータ
    user_sikaku_list = request.form.getlist('sikaku')

    # メールアドレスの重複がないか判定
    # judg = validation.check_mail(new_user_info['mail'])
    # print(type(judg))
    # print(judg)
    # if judg != True:
    #     message = 'メールアドレスが重複しています'
    #     user_id = session['user_id']
    #     user_name = session['user_name']
    #     return render_template('edit_user_info.html', message=message,
    #                            user_id=user_id, user_name=user_name)

    db = db_connect.DBconnect()
    message = db.update_user(user_id, new_user_info,
                             new_user_subinfo, user_sikaku_list)
    # return先を考えるredirectでuser_page()に飛ばす
    id = session['user_id']

    return redirect(url_for('user_page', id=id, message=message))


# アカウント削除
@app.route('/delete/<int:id>')
def account_delete(id):
    db = db_connect.DBconnect()
    message = db.delete_user(id)

    print('削除成功')

    return render_template('index.html', message=message)
