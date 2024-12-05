from app import db


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(8), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Ensure that no two assessments have the same title and module code
    __table_args__ = (
        db.UniqueConstraint('module_code', 'title', name='unique_module_title'),
    )
