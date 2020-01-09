from flask_script import Manager


def register_manage_commands(manager: Manager):
    @manager.command
    def create_admin():
        from app.user import UserService
        from app.user import UserInfoModel
        username = input('Input Username:')
        password = input('Input Password:')
        UserService().add_item(
            username=username, password=password, is_admin=True,
            info=UserInfoModel(comment='Create By Manager.')
        )
