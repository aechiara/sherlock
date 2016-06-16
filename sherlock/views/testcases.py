"""Sherlock Scenario Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g
from flask_login import login_required

from sherlock import db
from sherlock.data.model import Scenario, Project, Test_Case


test_case = Blueprint('test_cases', __name__)


@test_case.url_value_preprocessor
@login_required
def get_test_case(endpoint, values):
    """Blueprint Object Query."""
    project = Project.query.filter_by(id=values.pop('project_id'))
    scenario = Scenario.query.filter_by(id=values.pop('scenario_id'))
    if project and scenario:
        if 'test_case_id' in values:
            query = Test_Case.query.filter_by(id=values.pop('test_case_id'))
            g.test_case = query.first_or_404()


@test_case.route('/', methods=['GET'])
@login_required
def show():
    """Docstring."""
    return g.test_case


@test_case.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """POST endpoint for new scenarios.

    Param:
        name(required)
        scenario_name(required).
    """
    if request.method == 'POST':
        new_test_case = Test_Case(name=request.form['name'],
                                  scenario_id=request.form['scenario_id'],
                                  state_id=1)
        db.session.add(new_test_case)
        db.session.commit()
        return redirect(url_for('show', scenario_id=g.test_case.scenario_id))
    elif request.method == 'GET':
        pass
        # TODO return JSON.


@test_case.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """POST endpoint for editing existing scenarios.

    Param:
        name
        name
    """
    if request.method == 'POST':
        edited_tc = g.test_case
        edited_tc.name = request.form['scenario_name']

        db.session.add(edited_tc)
        db.session.commit()
        return redirect(url_for('test_cases.show', scenario_id=g.scenario.id))
    elif request.method == 'GET':
            pass
            # TODO render template of the form.