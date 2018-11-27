from rest_framework import status
from rest_framework.test import APITestCase
from .models import Candidate

from json import loads


class CandidateTests(APITestCase):

    def setUp(self):

        self.url = "/api/candidate/"
        with open("api/mockupdata/candidate.json", "r") as f:
            self.mock_up_data = loads(f.read())

    def test_create_candidate(self):

        for request_data in self.mock_up_data:
            response = self.client.post(self.url, request_data, format="json")
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

    def test_read_candidate(self):

        for instance_data in self.mock_up_data:
            instance = Candidate(id=1, **instance_data)
            response = self.client.get(self.url + str(instance.id) + "/", {}, format="json")
            # Check status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # Check the response data
            response_data = loads(response.content)
            self.assertEqual(response_data["annotation"], instance.annotation)
            self.assertEqual(response_data["name"], instance.name)
            self.assertEqual(response_data["surname"], instance.surname)
            self.assertEqual(response_data["is_student"], instance.is_student)

    def test_update_candidate(self):

        for instance_data in self.mock_up_data:
            for request_data in self.mock_up_data:
                instance = Candidate(id=1, **instance_data)
                response = self.client.put(self.url + str(instance.id) + "/", request_data, format="json")
                # Check status code
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                # Check the response data
                response_data = loads(response.content)
                for key in request_data:
                    self.assertEqual(request_data[key], response_data[key])
                # Check database data
                self.assertEqual(request_data["annotation"], instance.annotation)
                self.assertEqual(request_data["name"], instance.name)
                self.assertEqual(request_data["surname"], instance.surname)
                self.assertEqual(request_data["is_student"], instance.is_student)
