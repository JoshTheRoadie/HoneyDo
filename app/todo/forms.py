from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length


class AddNewTodoForm(FlaskForm):
    title = StringField('Add a new Honey-Do list:', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Add New Honey-Do')


class FollowUserForm(FlaskForm):
    username = StringField('Enter the name of the user you would like to follow:',
                           validators=[DataRequired(), Length(1, 64)])
    friend_code = StringField('Enter the friend code for this friend.',
                              validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Follow User')


class UnfollowUserForm(FlaskForm):
    username = StringField('Enter the name of the user you would like to unfollow:',
                           validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Unfollow User')


class AddNewTaskForm(FlaskForm):
    task = StringField('Add a new task to this Honey-Do list: ', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Add New Task')


class HoneyTestForm(FlaskForm):
    honeydo = QuerySelectMultipleField(get_label='task', allow_blank='False', validators=[DataRequired()])
    submit = SubmitField('Strike Task')