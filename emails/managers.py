from django.db.models.manager import Manager


class EmailManager(Manager):
    def send_pending(self):
        pending_emails = self.filter(sent=False)

        for email in pending_emails:
            email.send()
