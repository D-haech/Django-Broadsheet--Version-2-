from collections import defaultdict

from .models import StudentScore


def calculate_student_subject_result(
    student,
    subject,
    session,
    term,
):
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
            "raw_score": raw_score,
            "raw_maximum": raw_maximum,
            "weight": weight,
            "weighted_score": round(weighted_score, 2),
            "assessments": type_scores,
        }

    total = sum(item["weighted_score"] for item in results.values())

    return {
        "assessment_types": results,
        "total": round(total, 2),
    }
