from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APITestCase

from apps.crud_app.models import Event

EVENT = {
    "title": "Tech Meetup",
    "place": "Convention Center",
    "city": "Austin",
    "state": "TX",
    "zipcode": "73301",
    "category": "Technology",
    "start_date": "2026-03-10",
    "end_date": "2026-03-10",
}


class AuthenticatedTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("demo", password="s3cure-pass!")

    def sign_in(self):
        tokens = self.client.post("/api/auth/token/", {"username": "demo", "password": "s3cure-pass!"}).json()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return tokens


class EventReadTests(APITestCase):
    def setUp(self):
        call_command("seed_events", verbosity=0)

    def test_anyone_can_list_with_pagination(self):
        body = self.client.get("/api/events/").json()
        self.assertEqual(body["count"], 5)
        self.assertEqual(body["results"][0]["title"], "Tech Meetup")

    def test_search_filter_and_ordering(self):
        self.assertEqual(self.client.get("/api/events/?search=jazz").json()["count"], 1)
        self.assertEqual(self.client.get("/api/events/?category=technology").json()["count"], 2)
        self.assertEqual(self.client.get("/api/events/?state=ca").json()["results"][0]["city"], "San Francisco")
        newest = self.client.get("/api/events/?ordering=-start_date").json()["results"][0]
        self.assertEqual(newest["title"], "Data Science Conf")

    def test_detail_and_not_found(self):
        event = Event.objects.first()
        self.assertEqual(self.client.get(f"/api/events/{event.pk}/").status_code, 200)
        self.assertEqual(self.client.get("/api/events/999/").status_code, 404)


class EventWriteTests(AuthenticatedTestCase):
    def test_writes_require_a_token(self):
        self.assertEqual(self.client.post("/api/events/", EVENT).status_code, 401)

    def test_create_update_and_delete(self):
        self.sign_in()
        created = self.client.post("/api/events/", EVENT)
        self.assertEqual(created.status_code, 201)
        pk = created.json()["id"]
        patched = self.client.patch(f"/api/events/{pk}/", {"title": "Jazz Night"})
        self.assertEqual(patched.json()["title"], "Jazz Night")
        self.assertEqual(self.client.delete(f"/api/events/{pk}/").status_code, 204)
        self.assertFalse(Event.objects.exists())

    def test_validation_errors(self):
        self.sign_in()
        response = self.client.post(
            "/api/events/", {**EVENT, "state": "Texas", "zipcode": "ABC", "end_date": "2026-03-01"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()), {"state", "zipcode"})
        dates = self.client.post("/api/events/", {**EVENT, "end_date": "2026-03-01"})
        self.assertIn("end_date", dates.json())

    def test_refresh_token(self):
        tokens = self.sign_in()
        refreshed = self.client.post("/api/auth/token/refresh/", {"refresh": tokens["refresh"]})
        self.assertEqual(refreshed.status_code, 200)


class ApiDocsTests(APITestCase):
    def test_schema_and_swagger_ui(self):
        schema = self.client.get("/api/schema/?format=json")
        self.assertEqual(schema.status_code, 200)
        self.assertIn("/api/events/{id}/", schema.json()["paths"])
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)
