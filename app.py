from flask import Flask, request, session
from bot import ask, append_interaction_to_chat_log
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '89djhff9lhkd93'
basedir = os.path.abspath(os.getcwd())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chats_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()


class Users(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)


def get_data(unique_Id):
    try:
        return Users.query.get_or_404(unique_Id).data
    except Exception as e:
        user = Users(unique_id=unique_Id, data="")
        db.session.add(user)
        db.session.commit()
        return Users.query.get_or_404(unique_Id).data


def set_data(unique_Id, new_data):
    Users.query.filter_by(unique_id=unique_Id)[0].data = new_data
    db.session.commit()


@app.route('/bot', methods=['POST'])
def bot():
    user_id = request.values["Id"]
    incoming_msg = request.values['Body']
    chat_log = get_data(int(user_id))
    answer = ask(incoming_msg, chat_log)
    set_data(int(user_id), append_interaction_to_chat_log(incoming_msg, answer, chat_log))
    return str(answer)


if __name__ == '__main__':
    app.run(debug=True)
