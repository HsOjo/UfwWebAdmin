from app import db, Model


class RuleModel(db.Model, Model):
    __tablename__ = 'rule'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    number = db.Column(db.VARCHAR)
    src = db.Column(db.VARCHAR)
    src_eth = db.Column(db.VARCHAR)
    dest = db.Column(db.VARCHAR)
    dest_eth = db.Column(db.VARCHAR)
    action = db.Column(db.VARCHAR, index=True)
    direction = db.Column(db.VARCHAR, index=True)
    comment = db.Column(db.VARCHAR)
    is_v6 = db.Column(db.BOOLEAN, index=True)
