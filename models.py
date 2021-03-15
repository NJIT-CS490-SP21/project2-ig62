"""models.py"""
from app import DB


class Person(DB.Model):
    """Person class"""
    # Disable all the no-member violations in this function
    # pylint: disable=no-member
    id = DB.Column(DB.Integer)
    username = DB.Column(DB.String(80),
                         unique=True,
                         nullable=False,
                         primary_key=True)
    score = DB.Column(DB.Integer)

    def __repr__(self):
        return '<Person %r>' % self.username
