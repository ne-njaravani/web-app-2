from flask import Flask, render_template, redirect, url_for, flash, request
from app import app, db, models
from .forms import AssessmentForm
from sqlalchemy.exc import IntegrityError


# Display all the assessments grouping them by whether they are complete or incomplete
@app.route('/')
def home():
    in_progress_assessments = models.Assessment.query.filter_by(completed=False).all()
    completed_assessments = models.Assessment.query.filter_by(completed=True).all()
    return render_template('home.html', 
                           in_progress_assessments=in_progress_assessments, 
                           completed_assessments=completed_assessments)


# Create an assessment and add it to the database
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = AssessmentForm()
    if form.validate_on_submit():
        assessment = models.Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            description=form.description.data,
            deadline=form.deadline.data,
            completed=False
        )
        try:
            db.session.add(assessment)
            db.session.commit()
            flash('Assessment created successfully!', 'success')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('An assessment with this module code and title already exists. Please try again.', 'danger')
    return render_template('create.html', title= 'Create', form=form)


# Edit an assessment and save the changes to the database
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    assessment = models.Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        # Check for duplicates
        duplicate_assessment = models.Assessment.query.filter(
            models.Assessment.module_code == form.module_code.data,
            models.Assessment.title == form.title.data,
            models.Assessment.id != id
        ).first()        
        if duplicate_assessment:
            flash('An assessment with this module code and title already exists. Please try again.', 'danger')
        # Update assessment if no duplicates found
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.description = form.description.data
        assessment.deadline = form.deadline.data        
        try:
            db.session.commit()
            flash('Assessment updated successfully!', 'success')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while updating the assessment. Please try again.', 'danger')    
    return render_template('edit.html', form=form)



# Filter the assessments based on their completion status
@app.route('/completed')
def completed():
    assessments = models.Assessment.query.filter_by(completed=True).all()
    return render_template('completed.html', assessments=assessments)


@app.route('/uncompleted')
def uncompleted():
    assessments = models.Assessment.query.filter_by(completed=False).all()
    return render_template('uncompleted.html', assessments=assessments)


# Change the state of the assessment. Is it still in progress or is it still to be completed
@app.route('/toggle_complete/<int:id>')
def toggle_complete(id):
    assessment = models.Assessment.query.get_or_404(id)
    assessment.completed = not assessment.completed
    db.session.commit()
    flash('Assessment status updated successfully!', 'success')
    return redirect(url_for('home'))


# Delete an assessment and remove it from the database. Undo the delete, should any error occur
@app.route('/delete/<int:id>')
def delete_assessment(id):
    try:
        assessment = models.Assessment.query.get_or_404(id)
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assessment: {str(e)}', 'danger')
    return redirect(url_for('uncompleted'))

