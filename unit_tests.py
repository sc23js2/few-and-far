import unittest
from unittest.mock import patch
from config import ENDPOINTS
from collections import defaultdict
import requests, os
from main import fill_supporters, get_donations  

class TestDonationApp(unittest.TestCase):

    @patch("requests.get")
    def test_api_available(self, mock_get):
        """
            Test API availability
        """
        mock_get.return_value.status_code = 200

        url = ENDPOINTS.get_supporters()
        response = requests.get(url)

        self.assertTrue(response.status_code == 200)


    def test_directory_exists(self):
        """
        Test if the output directory exists
        """
        output_dir = "donation_output"
        os.makedirs(output_dir, exist_ok=True)
        self.assertTrue(os.path.exists(output_dir))


    @patch("requests.get")
    def test_fill_supporters(self, mock_get):
        """ 
        Test if supporters are correctly fetched and stored in the supporter_donations dictionary.
        """
        #Test data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": [
                {"id": "123", "name": "Jasmine", "donations": [], "created_at": "2022-01-01T12:00:00Z"},
                {"id": "987", "name": "Alex", "donations" : 0, "created_at": "2022-02-01T12:00:00Z"}
            ],
            "has_more": False
        }
        
        supporter_donations = defaultdict(dict)
        result = fill_supporters(supporter_donations)

        # Assert
        self.assertIn("123", result)
        self.assertEqual(result["123"]["name"], "Jasmine")


    @patch("requests.get")
    def test_get_donations(self, mock_get):
        """
        Test if donations are correctly fetched and stored to corresponding supporters.
        """
        #Test data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": [
                {"id": "1", "amount": 5000, "supporter_id": "123", "created_at": "2022-03-01T12:00:00Z"},
                {"id": "2", "amount": 2500, "supporter_id": "987", "created_at": "2022-03-02T12:00:00Z"}
            ],
            "has_more": False
        }

        # Mock the supporter_donations dictionary. simulating the output of fill_supporters
        supporter_donations = defaultdict(dict)
        supporter_donations["123"] = {"name": "Jasmine", "created_at": "2022-01-01T12:00:00Z", "donations": [], "total_donated": 0}
        supporter_donations["987"] = {"name": "Alex", "created_at": "2022-02-01T12:00:00Z", "donations": [], "total_donated": 0}

        donations = get_donations(supporter_donations)

        # Assert
        self.assertEqual(donations["123"]["total_donated"], 50.00)
        self.assertEqual(len(donations["123"]["donations"]), 1)

        self.assertEqual(donations["987"]["total_donated"], 25.00)
        self.assertEqual(len(donations["987"]["donations"]), 1)


if __name__ == "__main__":
    unittest.main()