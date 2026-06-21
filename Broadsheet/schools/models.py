from django.db import models
from accounts.models import User


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    classes = models.ManyToManyField("academics.SchoolClass",blank=True)

    phone = models.CharField(max_length=20, blank=True)
    subjects = models.ManyToManyField("academics.Subject", blank=True)

    address = models.TextField(blank=True)

    date_employed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class TeacherClass(models.Model):

    teacher = models.ForeignKey("schools.Teacher", on_delete=models.CASCADE)

    school_class = models.ForeignKey("academics.SchoolClass", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("teacher", "school_class")


class TeacherSubject(models.Model):

    teacher = models.ForeignKey("schools.Teacher", on_delete=models.CASCADE)

    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("teacher", "subject")


class TeachingAssignment(models.Model):

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    school_class = models.ForeignKey("academics.SchoolClass", on_delete=models.CASCADE)

    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE)

    class Meta:

        constraints = [
        models.UniqueConstraint(
            fields=[
                "teacher",
                "school_class",
                "subject",
            ],
            name="unique_teacher_assignment"
        )
    ]
    def __str__(self):

        return f"{self.teacher} - " f"{self.school_class} - " f"{self.subject}"
