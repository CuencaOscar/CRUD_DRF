from django.core.management.base import BaseCommand

from apps.crud_app.models import Event

DEMO_EVENTS = [
    ("Tech Meetup", "Convention Center", "Austin", "TX", "73301", "Technology", "2026-03-10", "2026-03-10"),
    ("Jazz Night", "Blue Note Hall", "Seattle", "WA", "98101", "Music", "2026-04-05", "2026-04-05"),
    ("Startup Summit", "Moscone Center", "San Francisco", "CA", "94103", "Business", "2026-05-12", "2026-05-14"),
    ("Food Truck Festival", "Centennial Park", "Nashville", "TN", "37203", "Food", "2026-06-20", "2026-06-21"),
    ("Data Science Conf", "Javits Center", "New York", "NY", "10001", "Technology", "2026-09-08", "2026-09-10"),
]


class Command(BaseCommand):
    help = "Load a few demo events (skips titles that already exist)."

    def handle(self, *args, **options):
        created = 0
        for title, place, city, state, zipcode, category, start, end in DEMO_EVENTS:
            _, was_created = Event.objects.get_or_create(
                title=title,
                defaults=dict(place=place, city=city, state=state, zipcode=zipcode, category=category,
                              start_date=start, end_date=end),
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} demo events created."))
