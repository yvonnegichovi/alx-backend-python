#!/usr/bin/env python3
"""
This module has tests
""" 

from client import GithubOrgClient
from parameterized import parameterized
from test_utils import get_json
from unittest.mock import patch
import unittest


class TestGithubOrgClient(unittest.TestCase):
    """
    The first class for this file. Focuses on parameterization and patch
    as decorators
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"key": "value"})
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"key": "value"})


    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        It mocks a property
        """
        mock_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        mock_org.return_value = mock_payload
        client = GithubOrgClient("test-org")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/test-org/repos")


if __name__ == "__main__":
    unittest.main()
