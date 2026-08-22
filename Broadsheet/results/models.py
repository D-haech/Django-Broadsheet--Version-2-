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


# Grading System(School Configured)
# results/models.py - Add these models at the end of the file


class GradeSystem(models.Model):
    """
    A grading system that a school can configure.
    Example: "Primary Grading" or "Secondary Grading"
    """

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g., Primary School Grading")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("school", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Grade(models.Model):
    """
    Individual grade levels within a grading system.
    Example: A (70-100), B (60-69), etc.
    """

    grade_system = models.ForeignKey(
        GradeSystem, on_delete=models.CASCADE, related_name="grades"
    )
    min_score = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Minimum score for this grade"
    )
    max_score = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Maximum score for this grade"
    )
    grade = models.CharField(max_length=5, help_text="e.g., A, B+, C-")
    remark = models.CharField(max_length=50, help_text="e.g., Excellent, Very Good")
    points = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        help_text="Grade points for GPA calculation",
    )
    position = models.PositiveIntegerField(
        default=0, help_text="Order of grades (1=highest)"
    )

    class Meta:
        ordering = ["position"]
        unique_together = ("grade_system", "grade")

    def __str__(self):
        return f"{self.grade} ({self.min_score} - {self.max_score})"

    def get_grade_and_remark(self, score):
        """
        Check if a score falls within this grade's range.
        """
        return self.min_score <= score <= self.max_score
