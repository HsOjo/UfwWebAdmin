from flask import render_template, Flask


def register_app_errors(app: Flask):
    @app.errorhandler(500)
    def error_500(e: Exception):
        return render_template('common/error.html', e=e), 500

    @app.errorhandler(404)
    def error_404(e: Exception):
        return render_template('common/error.html', e=e), 404

    @app.errorhandler(403)
    def error_403(e: Exception):
        return render_template('common/error.html', e=e), 403
