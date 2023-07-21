from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from typing import Dict, List
from rest_framework import status


class CustomersViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        #Url of Kombat viwe
        self.url: str = reverse("kombat")
    
    def test_valid_hits(self):

        """
            This test validate that the view only acept valid hits
            The valid hit are: P,K
        """

        #Data with invalid hit
        data_hit: Dict[str, str] = {
            "player1":{
                "movimientos":["D","DSD","S","DSD","SD"],
                "golpes":["K","P","","K","P","Q"]
            },
            "player2": {
                "movimientos":["SA","SA","SA","ASA","SA"],
                "golpes":["K","","K","P","P"]
            }
        }

        response = self.client.post(self.url, data_hit, format="json")
        #Validate the status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #Validate error message
        self.assertEqual(response.json(), {'golpes': ["The hit {'Q'} is invalid"]})

        #Data with invalid hit
        data_hit: Dict[str, str] = {
            "player1":{
                "movimientos":["D","DSD","S","DSD","SD"],
                "golpes":["K","P","","K","P"]
            },
            "player2": {
                "movimientos":["SA","SA","SA","ASA","SA"],
                "golpes":["K","","K","P","P","O"]
            }
        }

        response = self.client.post(self.url, data_hit, format="json")
        #Validate the status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #Validate error message
        self.assertEqual(response.json(), {'golpes': ["The hit {'O'} is invalid"]})

    def test_valid_moving(self):

        """
            This test validate that the view only acept valid moving
            The valid moving are: W,S,A,D
        """

        #Data with invalid moving
        data_moving: Dict[str, str] = {
            "player1":{
                "movimientos":["D","DSDT","S","DSD","SD"],
                "golpes":["K","P","","K","P"]
            },
            "player2": {
                "movimientos":["SA","SA","SA","ASA","SA"],
                "golpes":["K","","K","P","P"]
            }
        }

        response = self.client.post(self.url, data_moving, format="json")
        #Validate the status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #Validate error message
        self.assertEqual(response.json(), {'movimientos': ["The moving {'T'} is invalid"]})

        #Data with invalid moving
        data_moving: Dict[str, str] = {
            "player1":{
                "movimientos":["D","DSD","S","DSD","SD"],
                "golpes":["K","P","","K","P"]
            },
            "player2": {
                "movimientos":["SA","SA","SA","ASAO","SA"],
                "golpes":["K","","K","P","P"]
            }
        }

        response = self.client.post(self.url, data_moving, format="json")
        #Validate the status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #Validate error message
        self.assertEqual(response.json(), {'movimientos': ["The moving {'O'} is invalid"]})

    def test_valid_input(self):

        """
            This test validate that the view only acept valid moving
            The valid moving are: W,S,A,D
        """

        #Data with invalid moving
        data_moving: Dict[str, str] = {
            "player1":{
                "movimientos":["D","DSD","S","DSD","SD"],
                "golpes":["K","P","","K","P"]
            },
            "player2": {
                "movimientos":["SA","SA","SA","ASA","SA"],
                "golpes":["K","","K","P","P"]
            }
        }

        response = self.client.post(self.url, data_moving, format="json")
        #Validate the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #Validate error message
        json_response: List[str] = [
            "Tonyn avanza y da una patada",
            "Arnaldor usa un Remuyuke",
            "Tonyn usa un Taladoken",
            "Arnaldor se mueve",
            "Tonyn se mueve",
            "Arnaldor usa un Remuyuke",
            "Arnaldor gana la pelea y aun le queda 2 de energia"
        ]
        self.assertEqual(response.json(), json_response)