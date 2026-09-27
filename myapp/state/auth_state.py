import reflex as rx


class AuthState(rx.State):
    user_id: str = ""
    user_name: str = ""
    user_email: str = ""
    is_authenticated: bool = False

    @rx.event
    def set_user(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.user_name = name
        self.user_email = email
        self.is_authenticated = True

    @rx.event
    def logout(self):
        self.user_id = ""
        self.user_name = ""
        self.user_email = ""
        self.is_authenticated = False
        return rx.redirect("/")