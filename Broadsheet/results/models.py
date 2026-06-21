from django.db import models

# Create your models here.


class AssessmentType(models.Model):

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=50,
    )

    maximum_score = models.PositiveIntegerField()

    class Meta:

        unique_together = (
            "school",
            "name",
        )

        ordering = ["name"]

    def __str__(self):

        return self.name


class Assessment(models.Model):

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    maximum_score = models.PositiveIntegerField()

    def __str__(self):

        return f"{self.assessment_type.name} - " f"{self.name}"


class StudentScore(models.Model):

    student = models.ForeignKey("academics.Student", on_delete=models.CASCADE)

    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE)

    session = models.ForeignKey("academics.Session", on_delete=models.CASCADE)

    term = models.ForeignKey("academics.Term", on_delete=models.CASCADE)

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)

    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:

        unique_together = (
            "student",
            "subject",
            "session",
            "term",
            "assessment",
        )

    def __str__(self):

        return f"{self.student} - " f"{self.subject} - " f"{self.assessment}"
