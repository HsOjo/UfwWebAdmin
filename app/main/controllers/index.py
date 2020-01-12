from flask import render_template, request, flash, redirect

from app.lib import Ufw
from app.main.base import UfwController
from app.main.common import ufw_status
from app.main.forms.status import StatusForm


class IndexController(UfwController):
    import_name = __name__
    url_prefix = '/'

    def register_routes(self):
        self.register_route(self.index, '/')
        self.register_route(self.index)
        self.register_route(self.edit, methods=['GET', 'POST'])

    def index(self):
        status = ufw_status(self.ufw, 3)
        default = status.pop('default', None)
        return render_template('main/index.html', status=status, default=default)

    def edit(self):
        status = ufw_status(self.ufw, 3)
        status.update(**status.pop('default'))
        form = StatusForm()
        if request.method == 'POST' and form.validate_on_submit():
            for k, v in status.items():
                fv = form.data.get('k')
                if fv is not None and fv != v:
                    if k == 'status':
                        if fv == Ufw.STATUS_ACTIVE:
                            self.ufw.enable()
                        elif fv == Ufw.STATUS_INACTIVE:
                            self.ufw.disable()
                    elif k == 'logging' or k == 'logging_level':
                        self.ufw.logging(fv)
                    elif k == 'incoming' or k == 'outgoing' or k == 'routed':
                        self.ufw.default(fv, k)
            flash('Edit Success', 'success')
            return redirect(self.url_for(self.index))
        else:
            form.inject_data(**status)

        return render_template('main/edit.html', form=form)
