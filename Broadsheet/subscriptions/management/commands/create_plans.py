from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan


class Command(BaseCommand):
    help = "Create default subscription plans"

    def handle(self, *args, **options):
        plans = [
            {
                "name": "Basic",
                "description": "Perfect for small schools getting started",
                "price": 5000.00,
                "duration_days": 90,
                "student_limit": 100,
                "teacher_limit": 10,
                "has_broadsheet": True,
                "has_report_cards": True,
                "has_analytics": False,
                "is_default": True,
            },
            {
                "name": "Standard",
                "description": "Ideal for growing schools with more needs",
                "price": 10000.00,
                "duration_days": 90,
                "student_limit": 500,
                "teacher_limit": 50,
                "has_broadsheet": True,
                "has_report_cards": True,
                "has_analytics": True,
                "is_default": False,
            },
            {
                "name": "Premium",
                "description": "Full-featured for large schools and institutions",
                "price": 20000.00,
                "duration_days": 90,
                "student_limit": 2000,
                "teacher_limit": 200,
                "has_broadsheet": True,
                "has_report_cards": True,
                "has_analytics": True,
                "is_default": False,
            },
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data["name"], defaults=plan_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created plan: {plan.name}"))
            else:
                self.stdout.write(f"Plan already exists: {plan.name}")
