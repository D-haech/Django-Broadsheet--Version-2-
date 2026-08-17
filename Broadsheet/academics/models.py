from django.db import models


# Create your models here.
class Session(models.Model):

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    name = models.CharField(max_length=20)

    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Term(models.Model):

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    name = models.CharField(max_length=20)

    is_current = models.BooleanField(default=False)


    def save(self, *args, **kwargs):

        if self.is_current:

            Term.objects.filter(
            school=self.school).update(
            is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session} - {self.name}"


class Subject(models.Model):

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    sex = (("Male", "Male"), ("Female","Female"))
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=20, verbose_name='First Name')
    surname = models.CharField(verbose_name='Surname', max_length=50)
    mid_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Middle Name')
    admission_no = models.CharField( max_length=50, blank=True, null=True, verbose_name="Admission Number")
    gender = models.CharField(choices=sex, max_length=50)
    date_of_birth = models.DateField()
    passport = models.ImageField(upload_to="students/", null=True, blank=True)
    
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['surname']
        constraints = [models.UniqueConstraint
                       (fields=["school", "admission_no"], 
                        name="unique_admission_per_school")]

    def __str__(self):
        return f'{self.surname} {self.first_name}'
