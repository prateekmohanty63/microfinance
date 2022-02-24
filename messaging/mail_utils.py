from django.core.mail import send_mail
from django.conf import settings

class SendMail:
    def __init__(self, recipient_name: str, link: str, recipient_list: list, subject: str, mail_for: str):
        self.recipient_name = recipient_name
        self.link = link
        self.from_email = settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        self.subject = subject

        if mail_for == "sign-up":
            self.content = self.__sign_up_compose_mail()
        if mail_for == "sign-up-alert":
            self.content = self.__sign_up_alert_compose_mail()
        elif mail_for == "reset-password":
            self.content = self.__reset_password_compose_mail()
        elif mail_for == "password-change":
            self.content = self.__password_change_compose_mail()
        elif mail_for == "account-confirm-alert":
            self.content = self.__account_confirm_alert_compose_mail()

    def __sign_up_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        Thanks so much for signing up for Microfinance!\n
        Use the link below to confirm your account:\n
        {self.link}\n
        If you didn't sign up for Microfinance, please ignore this email.\n
        Sincerely,\n
        Microfinance Support
        """
        print(content)
        return content

    def __sign_up_alert_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        A new user registered for Microfinance!\n
        Sincerely,\n
        Microfinance Support
        """
        print(content)
        return content

    def __reset_password_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        We received a request to change the password for the account with the email {self.recipient_list}\n
        Use the link below to reset your password:\n
        {self.link}\n
        If you don't want to reset your password or you did not request this change, you can ignore this email.\n
        Sincerely,\n
        Microfinance Support
        """
        print(content)
        return content

    def __password_change_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        Your Microfinance password for the account with the email {self.recipient_list} has changed. \n
        If you did not reset your password or you did not request this change, please get in touch with support as soon as possible.\n
        Sincerely,\n
        Microfinance Support
        """
        print(content)
        return content

    def __account_confirm_alert_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        A new account was confirmed. \n
        Sincerely,\n
        Microfinance Support
        """
        print(content)
        return content

    def send(self):
        try:
            send_mail(subject=self.subject, message=self.content, from_email='Microfinance <' + self.from_email + '>', recipient_list=[self.recipient_list], fail_silently=True)
            return True
        except Exception:
            return False
