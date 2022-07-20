from django.db import models
from student.models import Student

class SuperVisor(models.Model):
    supervisor_name = models.TextField()
    student1_id = models.IntegerField()
    student2_id = models.IntegerField()

    def get_students(self):
        student1 = Student.objects.get(id=self.student1_id)
        student2 = Student.objects.get(id=self.student2_id)
        return [student1, student2]

def get_students(supervisor):
    st = []
    students = Student.objects.all()
    # print(supervisor.id)
    for student in students:
        # print(student.supervisor_id)
        if student.supervisor_id == supervisor.id:
            st.append(student)
    return st
# Create your models here.
