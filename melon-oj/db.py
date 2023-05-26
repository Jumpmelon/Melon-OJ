import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Problem(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(128), nullable=False)
    statement = sa.Column(sa.Text, nullable=False)
    visibility = sa.Column(
        sa.Enum("Private", "Public"), nullable=False, default="Private"
    )


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32), unique=True)
    _password = sa.Column(sa.String(128), nullable=False)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        from werkzeug.security import generate_password_hash

        self._password = generate_password_hash(value)

    def check_password(self, value: str) -> bool:
        from werkzeug.security import check_password_hash

        return check_password_hash(self._password, value)


class ProblemManager(db.Model):
    problem_id = sa.Column(sa.ForeignKey(Problem.id), primary_key=True)
    manager_id = sa.Column(sa.ForeignKey(User.id), primary_key=True)


class Submission(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    problem_id = sa.Column(sa.ForeignKey(Problem.id))
    user_id = sa.Column(sa.ForeignKey(User.id))
    answer = sa.Column(sa.Text, nullable=False)
    time = sa.Column(sa.DateTime)
    verdict = sa.Column(
        sa.Enum("Waiting", "Judging", "Accepted", "Wrong Answer"),
        nullable=False,
        default="Waiting",
    )
    score = sa.Column(sa.Float)  # ranging [0.0, 1.0] in most cases


class Contest(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(128), nullable=False)
    start_time = sa.Column(sa.DateTime)
    end_time = sa.Column(sa.DateTime)


class ContestManager(db.Model):
    contest_id = sa.Column(sa.ForeignKey(Contest.id), primary_key=True)
    manager_id = sa.Column(sa.ForeignKey(User.id), primary_key=True)


class ContestProblem(db.Model):
    contest_id = sa.Column(sa.ForeignKey(Contest.id), primary_key=True)
    # index of the problem inside the contest
    idx = sa.Column(sa.Integer, primary_key=True)
    problem_id = sa.Column(sa.ForeignKey(Problem.id))
    score = sa.Column(sa.Float)


class ContestSubmission(db.Model):
    contest_id = sa.Column(sa.ForeignKey(Contest.id), nullable=False)
    idx = sa.Column(sa.Integer, nullable=False)
    submission_id = sa.Column(sa.ForeignKey(Submission.id), primary_key=True)
    sa.ForeignKeyConstraint(
        (contest_id, idx), (ContestProblem.contest_id, ContestProblem.idx)
    )
