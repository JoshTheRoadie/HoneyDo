from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from . import todo
from .forms import AddNewTodoForm, AddNewTaskForm, FollowUserForm, UnfollowUserForm, HoneyTestForm
from .. import db
from ..models import User, ToDo, Task


@todo.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    todo_form = AddNewTodoForm()
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo.home'))
    return render_template('todo/home.html', todo_form=todo_form)


@todo.route('/follow_user', methods=['GET', 'POST'])
@login_required
def follow_user():
    follow_form = FollowUserForm()
    if follow_form.validate_on_submit():
        friend_name = follow_form.username.data
        friend_code = follow_form.friend_code.data
        friend = User.query.filter(User.username == friend_name).first()
        if friend:
            if friend.friend_code == friend_code:
                current_user.follow(friend)
                flash('You are now following {}'.format(friend.username))
            else:
                flash('I am sorry.  It seems the friend code you entered is invalid.')
                return redirect(url_for('todo.follow_user'))
            return redirect(url_for('todo.home'))
        else:
            flash('I am sorry.  It seems that user is not in our database.  Please check the spelling of their name.')
    return render_template('todo/follow_user.html', follow_form=follow_form)


@todo.route('/unfollow_user', methods=['GET', 'POST'])
@login_required
def unfollow_user():
    unfollow_form = UnfollowUserForm()
    if unfollow_form.validate_on_submit():
        friend_name = unfollow_form.username.data
        if friend_name in [user.username for user in current_user.followed]:
            current_user.unfollow(User.query.filter(User.username == friend_name).first())
            flash('You have stopped following {}.'.format(friend_name))
            return redirect(url_for('todo.home'))
        else:
            flash('I am sorry.  You are not following the entered user.')
            return redirect(url_for('todo.unfollow_user'))
    return render_template('todo/unfollow_user.html', unfollow_form=unfollow_form)


@todo.route('/add_task/<todo_id>', methods=['GET', 'POST'])
@login_required
def add_task(todo_id):
    task_form = AddNewTaskForm()
    current_todo = ToDo.query.filter(ToDo.id == int(todo_id)).first()
    if task_form.validate_on_submit():
        new_task = Task(task=task_form.task.data, todo_id=current_todo.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('todo.home'))
    return render_template('todo/add_task.html', form=task_form, current_todo=current_todo)


@todo.route('/btn_test', methods=['GET', 'POST'])
def btn_test():
    if request.form.get('btn'):
        print request.form['btn']
        return redirect(url_for('todo.btn_test'))
    return render_template('todo/btn_test.html')


@todo.route('/honey_test/<todo_id>', methods=['GET', 'POST'])
def honey_test(todo_id):
    form = HoneyTestForm()
    form.honeydo.query = Task.query.filter(Task.todo_id == int(todo_id))
    title = ToDo.query.filter(ToDo.id == int(todo_id)).first().title
    if form.validate_on_submit():
        print form.honeydo.data
        return redirect(url_for('todo.honey_test', todo_id=todo_id))
    return render_template('todo/honey_test.html', title=title, form=form)
