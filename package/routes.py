from flask import render_template, url_for, flash, redirect, request
from package import app, db
from flask_login import LoginManager, UserMixin
from package.forms import RegistrationForm, LoginForm, ExpenseForm, IncomeForm, SavingsGoalForm, ContributionForm
from package.model import User, Expense, Income, SavingsGoal
from flask_login import login_user, login_required, logout_user, current_user
from decimal import Decimal


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route('/register',  methods=['GET', 'POST'])
def register_page():
    form=RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        existing_username = User.query.filter_by(username=form.username.data).first()

        if existing_username:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register_page'))
        if existing_user:
            flash('Email already exists. Please choose a different email.', 'danger')
            return redirect(url_for('register_page'))
        
        user_to_create = User(username=form.username.data,email=form.email.data,password_hash=form.password.data)

        db.session.add(user_to_create)
        db.session.commit()
        
        flash('Account created successfully!', category='success')
        return redirect(url_for('dashboard_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    attempted_user = User.query.filter_by(email=form.email.data).first()

    if form.validate_on_submit():

        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("Logged in successfully", category='success')
            return redirect(url_for('dashboard_page'))
    
        else:
            flash('Username or password is wrong', category='danger')

    return render_template('login.html',form=form)

@app.route("/dashboard")
@login_required
def dashboard_page():
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar()
    total_income = total_income if total_income is not None else 0

    total_expense = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar()
    total_expense = total_expense if total_expense is not None else 0

    remaining_income = total_income - total_expense

    total_contributions = db.session.query(db.func.sum(SavingsGoal.current_amount)).filter_by(user_id=current_user.id).scalar()
    total_contributions = total_contributions if total_contributions is not None else 0
    remaining_income -= total_contributions

    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expense, remaining_income=remaining_income)



@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home_page'))

@app.route('/income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()   
    if form.validate_on_submit():

        income = Income(amount=form.amount.data, source=form.source.data,user_id=current_user.id)
        
        db.session.add(income)
        db.session.commit()

        flash('Income added!', 'success')
        return redirect(url_for('dashboard_page'))
    
    return render_template('income.html', form=form)


@app.route('/expense', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar()

        expense = Expense(amount=form.amount.data, category=form.category.data, user_id=current_user.id)

        if form.amount.data < total_income:
            db.session.add(expense)
            db.session.commit()
            flash('Expense has been added', 'success')
            return redirect(url_for('dashboard_page'))
        
        else:
            flash('Expense amount cannot exceed total income!', 'danger')
    
    return render_template('expense.html', form=form)


@app.route('/saving_goal', methods=['GET', 'POST'])
@login_required
def saving_goal():
    goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    form = SavingsGoalForm()

    if form.validate_on_submit():
        goal_amount = form.goal_amount.data
        description = form.description.data

        new_goal = SavingsGoal(goal_amount=goal_amount, description=description, user_id=current_user.id)
        db.session.add(new_goal)
        db.session.commit()
        flash('New savings goal added successfully!', 'success')
        
        return redirect(url_for('saving_goal'))
    
    saving_goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    contribution_form = ContributionForm()

    return render_template('saving_goal.html', form=form, saving_goals=saving_goals, contribution_form=contribution_form)

@app.route('/contribute_goal/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def contribute_goal(goal_id):
    goal = SavingsGoal.query.get_or_404(goal_id)
    form = ContributionForm()
    
    if form.validate_on_submit():
        contribution = Decimal(form.amount.data)
        goal_amount = Decimal(goal.goal_amount)
        current_amount = Decimal(goal.current_amount)
        goal_amount_remaining = goal_amount - current_amount

        if contribution > goal_amount_remaining:
            flash('Contribution exceeds the remaining amount needed for the goal!', 'danger')
            return redirect(url_for('contribute_goal', goal_id=goal_id))
    
        goal.current_amount = current_amount + contribution
        
        total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar()
        total_income = Decimal(total_income) if total_income is not None else Decimal('0.00')
        remaining_income = total_income - contribution

        db.session.commit()

        flash('Contribution added successfully!', 'success')
        return redirect(url_for('saving_goal'))

    return render_template('contribute_goal.html', form=form, goal=goal)



@app.route('/reports')
@login_required
def reports():
    recent_incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).limit(5).all()
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()

    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar()
    total_income = Decimal(total_income) if total_income is not None else Decimal('0.00')

    total_contributions = db.session.query(db.func.sum(SavingsGoal.current_amount)).filter_by(user_id=current_user.id).scalar()
    total_contributions = Decimal(total_contributions) if total_contributions is not None else Decimal('0.00')

    return render_template('reports.html', 
                           recent_incomes=recent_incomes,
                           recent_expenses=recent_expenses)










