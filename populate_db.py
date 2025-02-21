import django
import os

# 🔹 Configure Django si le script est exécuté en dehors du projet
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.models import User
from polls.models import Teacher, Course

def create_teachers_and_courses():
    teacher_names = ["Alice", "Bob", "Charlie", "David", "Emma"]
    course_names = ["Math", "Physics", "Biology", "History", "Computer Science"]

    teachers = []
    for name in teacher_names:
        user, _ = User.objects.get_or_create(username=name, defaults={"password": "password123"})
        teacher, created = Teacher.objects.get_or_create(user=user)
        teachers.append(teacher)
        print(f"✅ Teacher created: {teacher}")

    for i, name in enumerate(course_names):
        teacher = teachers[i % len(teachers)]  # 🔹 Associe un cours à un enseignant
        course, created = Course.objects.get_or_create(name=name, teacher=teacher)
        print(f"✅ Course created: {course} (Teacher: {teacher.user.username})")

if __name__ == "__main__":
    create_teachers_and_courses()
