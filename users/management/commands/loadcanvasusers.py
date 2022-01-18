from django.core.management.base import BaseCommand, CommandError
from users.models import User
import canvasapi


CANVAS_URL = 'https://utexas.instructure.com'


class Command(BaseCommand):
    help = 'Bulk load users from Canvas'

    def add_arguments(self, parser):
        pass

    @staticmethod
    def get_names(full_name: str):
        tokens = full_name.split(' ', 1)
        return tokens[0], tokens[1]

    @staticmethod
    def load_users(canvas, course: canvasapi.canvas.Course):
        users = course.get_users()
        django_users = []

        for u in users:
            first, last = Command.get_names(u.name)
            django_users.append(User(
                first_name=first,
                last_name=last,
                eid=u.sis_user_id,
            ))

        User.objects.bulk_create(django_users, ignore_conflicts=True)

    def handle(self, *args, **options):
        token = input("Enter user token: ")
        canvas = canvasapi.Canvas(CANVAS_URL, token)
        user = canvas.get_current_user()
        courses = user.get_courses()
        courses = [c for c in courses]
        valid_courses = [False for i in range(len(courses))]

        print("Select a course")
        for i in range(len(courses)):
            try:
                if courses[i].enrollments[0]['type'] != 'student':
                    valid_courses[i] = True
                    print(f"{i} - {courses[i].name}")
            except AttributeError:
                pass

        number = int(input("Enter a number: "))

        if valid_courses[number]:
            confirm = input(f"Load users from course: {courses[number].name}? [Y/n]: ")
            if confirm in ['y', 'Y']:
                self.load_users(canvas, courses[number])
        else:
            print("Invalid course selected")
