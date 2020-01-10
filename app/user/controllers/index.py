from flask import render_template, request, flash, redirect
from flask_login import login_required, logout_user, login_user

from app.base import Controller
from app.user.forms import LoginForm
from app.user.services import UserService


class IndexController(Controller):
    import_name = __name__
    url_prefix = '/user'

    def register_routes(self):
        self.register_route(self.login, methods=['GET', 'POST'])
        self.register_route(self.logout)

    def login(self):
        form = LoginForm()
        service = UserService()

        if request.method == 'POST' and form.validate_on_submit():
            user = service.login(form.username.data, form.password.data)
            if user:
                flash('Login Successfully.', 'success')
                login_user(user, form.remember.data)
                next_path = request.args.get('next', request.path)
                return redirect(next_path)
            else:
                raise Exception('Username or Password Incorrect.')

        return render_template('user/login.html', form=form)

    @login_required
    def logout(self):
        if logout_user():
            flash('Logout Successfully.', 'success')
            return redirect('/user/login')
