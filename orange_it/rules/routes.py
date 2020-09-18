from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from orange_it import db
from orange_it.models import Rule, Thread
from orange_it.rules.forms import (RuleForm)

rules = Blueprint('rules', __name__)


@rules.route('/rule/new/<int:thread_id>', methods=['POST', 'GET'])
@login_required
def new_rule(thread_id):
    form = RuleForm()
    thread = Thread.query.get_or_404(thread_id)
    if form.validate_on_submit():
        rule = Rule(title=form.title.data, content=form.content.data, thread_id=thread_id)
        db.session.add(rule)
        db.session.commit()
        flash('A rule has been created for thread '+thread.title+'.', 'success')
        return redirect(url_for('thread.manage_thread', thread_id=thread.id) )
    return render_template('new_rule.html', title='Add a New Rule', form=form, legend='Create Rule')



@rules.route('/rule/<int:rule_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    form = RuleForm()
    if form.validate_on_submit():
        rule.title = form.title.data
        rule.content = form.content.data
        db.session.commit()
        flash('Your rule has been updated!', 'success')
        return redirect(url_for('rule', rule_id=rule_id))
    elif request.method == 'GET':
        form.title.data = rule.title
        form.content.data = rule.content
    return render_template('create_rule.html', title='Update Rule', form=form, legend="Update Rule")


@rules.route("/rule/<int:rule_id>/delete", methods=['POST'])
@login_required
def delete_post(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    # todo change current user to thread owner
    if rule.author != current_user:
        abort(403)
    db.session.delete(rule)
    db.session.commit()
    flash('Your rule has been deleted!', 'success')
    # todo change to go to update thread
    return redirect(url_for('main.index'))