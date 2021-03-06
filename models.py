from app import db
from datetime import datetime

user_identifier = db.Table('user_identifier',
    db.Column('user_index', db.Integer, db.ForeignKey('users.index')),
    db.Column('match_index', db.Integer, db.ForeignKey('matches.index'))
)

class User(db.Model):
    __tablename__ = 'users'

    index = db.Column(db.Integer, primary_key=True)
    slack_id = db.Column(db.String(80), unique=True)
    intra_id = db.Column(db.String(80), unique=True)
    register = db.Column(db.Boolean)
    joined = db.Column(db.Boolean)

    def __init__(self, slack_id, intra_id):
        self.slack_id = slack_id
        self.intra_id = intra_id
        self.register = True
        self.joined = False

    def __repr__(self):
        return '<index: {}, slack_id: {}, intra_id: {}, register: {}, joined: {}>'.format(self.index, self.slack_id, self.intra_id, self.register, self.joined)

    def serialize(self):
        return {
            'index': self.index,
            'slack_id': self.slack_id,
            'intra_id': self.intra_id,
            'register': self.register,
            'joined': self.joined
        }

class Match(db.Model):
    __tablename__ = 'matches'
    index = db.Column(db.Integer, primary_key=True)
    match_day = db.Column(db.DateTime)
    users = db.relationship(User, secondary=user_identifier, backref='matches')

    def __init__(self, user1, user2):
        self.match_day = datetime.now()
        self.users.append(user1)
        self.users.append(user2)

    def __repr__(self):
        return '<match_day: {}, user1_intra_id: {}, user2_intra_id: {}>'.format(self.match_day, self.users[0].intra_id,
                                                                                self.users[1].intra_id)

    def serialize(self):
        return {
            'match_day': self.match_day,
            'user1_intra_id': self.users[0].intra_id,
            'user2_intra_id': self.uesrs[1].intra_id,
        }



