from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.crud_app.models import Crud

EVENT = {
    "title": "Tech Meetup",
    "place": "Convention Center",
    "city": "Austin",
    "state": "Texas, TX",
    "zipcode": "73301",
    "other": "Networking",
    "start_date": "2024-03-10",
    "end_date": "2024-03-10",
    "category": "Technology",
}


class CrudApiTests(APITestCase):
    def test_create_and_list(self):
        response = self.client.post("/api/events/create/", EVENT)
        self.assertEqual(response.status_code, 201)
        listing = self.client.get("/api/events/read/").json()
        self.assertEqual(len(listing), 1)
        self.assertEqual(listing[0]["title"], "Tech Meetup")

    def test_invalid_payload_is_rejected(self):
        response = self.client.post("/api/events/create/", {**EVENT, "state": "Not a state"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Crud.objects.count(), 0)

    def test_update_and_delete(self):
        event = Crud.objects.create(**EVENT)
        response = self.client.post(f"/api/events/update/{event.pk}", {**EVENT, "title": "Jazz Night"})
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.title, "Jazz Night")
        self.assertEqual(self.client.delete(f"/api/events/delete/{event.pk}").status_code, 204)
        self.assertFalse(Crud.objects.exists())

    def test_missing_record_returns_404(self):
        self.assertEqual(self.client.post("/api/events/update/999", EVENT).status_code, 404)
        self.assertEqual(self.client.delete("/api/events/delete/999").status_code, 404)


class JwtTests(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user("demo", password="s3cure-pass!")

    def test_protected_view_requires_a_token(self):
        self.assertEqual(self.client.get("/api/events/protegida/").status_code, 401)

    def test_token_grants_access(self):
        tokens = self.client.post("/api/events/token/", {"username": "demo", "password": "s3cure-pass!"}).json()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        self.assertEqual(self.client.get("/api/events/protegida/").status_code, 200)
        refreshed = self.client.post("/api/events/token/refresh/", {"refresh": tokens["refresh"]})
        self.assertEqual(refreshed.status_code, 200)
