from rest_framework import status
from rest_framework.test import APITestCase
from .models import Candidate

from json import loads


class CandidateTests(APITestCase):

    def test_create_vote(self):

        url = "/api/candidate/"
        with open("api/mockupdata/candidate.json", "r") as f:
            mock_up_data = loads(f.read())
        for request_data in mock_up_data:
            response = self.client.post(url, request_data, format="json")
            # Check status code
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            # Check the response data
            response_data = loads(response.content)
            for key in request_data:
                self.assertEqual(request_data[key], response_data[key])
            # Check database data
            instance = Candidate.objects.filter(id=response_data["id"])[0]
            self.assertEqual(request_data["annotation"], instance.annotation)
            self.assertEqual(request_data["name"], instance.name)
            self.assertEqual(request_data["surname"], instance.surname)
            self.assertEqual(request_data["is_student"], instance.is_student)

