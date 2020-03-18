from flask_admin import Admin
from modules.say.controllers.hello import Hello

admin = Admin(name="admin")
admin.add_view(Hello(name="say.hello", url="/say/hello"))
