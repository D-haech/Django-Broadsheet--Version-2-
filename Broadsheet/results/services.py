from collections import defaultdict
from math import ceil

from .models import StudentScore


from collections import defaultdict


# results/services.py
from collections import defaultdict
from math import ceil
from .models import StudentScore, GradeSystem, Grade


def calculate_student_subject_result(student, subject, session, term):
    scores = StudentScore.objects.filter(
        student=student,
        subject=subject,
        session=session,
        term=term,
    ).select_related(
        "assessment",
        "assessment__assessment_type",
    )

    assessment_types = defaultdict(list)

    for student_score in scores:
        assessment_type = student_score.assessment.assessment_type
        assessment_types[assessment_type].append(student_score)

    results = {}

    for assessment_type, type_scores in assessment_types.items():
        raw_score = sum(score.score for score in type_scores)
        raw_maximum = sum(score.assessment.maximum_score for score in type_scores)
        weight = assessment_type.maximum_score

        if raw_maximum > 0:
            weighted_score = (raw_score / raw_maximum) * weight
        else:
            weighted_score = 0

        results[assessment_type.name] = {
            "raw_score": ceil(raw_score),
            "raw_maximum": ceil(raw_maximum),
            "weight": ceil(weight),
            "weighted_score": ceil(weighted_score),
            "assessments": type_scores,
        }

    total = sum(item["weighted_score"] for item in results.values())

    return {
        "assessment_types": results,
        "total": ceil(total),
    }


def get_grade_and_remark(score, school):
    """
    Get grade and remark for a score based on the school's active grading system.
    """
    try:
        # Get the active grading system for this school
        grade_system = GradeSystem.objects.filter(school=school, is_active=True).first()

        if not grade_system:
            # Fallback to default grading if no system configured
            return get_default_grade_and_remark(score)

        # Find the grade that matches this score
        grade = Grade.objects.filter(
            grade_system=grade_system, min_score__lte=score, max_score__gte=score
        ).first()

        if grade:
            return grade.grade, grade.remark
        else:
            # If score doesn't fall in any range, return default
            return get_default_grade_and_remark(score)

    except Exception:
        # Fallback in case of any error
        return get_default_grade_and_remark(score)


def get_default_grade_and_remark(score):
    """
    Default grading system if no database configuration exists.
    """
    if score >= 70:
        return "A", "Excellent"
    elif score >= 60:
        return "B", "Very Good"
    elif score >= 50:
        return "C", "Good"
    elif score >= 45:
        return "D", "Pass"
    elif score >= 40:
        return "E", "Fair"
    else:
        return "F", "Fail"
