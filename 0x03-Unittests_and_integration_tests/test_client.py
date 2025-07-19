#!/usr/bin/env python3
"""
This module has tests
"""

from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, Mock, PropertyMock
from utils import get_json
import fixtures
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
        expected_payload = {
            "login": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
            }
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected_payload)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        It mocks a property
        """
        mock_payload = {
                "repos_url": "https://api.github.com/orgs/test-org/repos"}
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload

            client = GithubOrgClient("test_org")

            result = client._public_repos_url

            mock_org.assert_called_once()

            self.assertEqual(result, mock_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        This method does more patching
        """
        test_repos_payload = [
            {"name": "repo_1", "license": {"key": "mit"}},
            {"name": "repo_2", "license": {"key": "apache-2.0"}},
            {"name": "repo_3", "license": {"key": "gpl-3.0"}},
        ]
        mock_get_json.return_value = test_repos_payload

        test_public_repos_url = "https://api.github.com/orgs/test_org/repos"

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_public_repos_url

            client = GithubOrgClient("test_org")

            repos = client.public_repos()

            self.assertEqual(repos, ["repo_1", "repo_2", "repo_3"])

            mock_public_repos_url.assert_called_once()

            mock_get_json.assert_called_once()

            repos_with_license = client.public_repos(license="apache-2.0")
            self.assertEqual(repos_with_license, ["repo_2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos method.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up class method to start patching requests.get.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop patching requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)


class MockResponse:
    """
    Mock response for requests.get.
    """
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos without license argument.
        """
        mock_get_json.side_effect = [
                Mock(json=Mock(return_value=fixtures.org_payload)),
                Mock(json=Mock(return_value=fixtures.repos_payload))
        ]

        client = GithubOrgClient("google")
        result = client.public_repos()

        self.assertEqual(result, fixtures.expected_repos)
        mock_get_json.assert_called_with("https://api.github.com/orgs/google")
        mock_get_json.assert_called_with(
                "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos with license="apache-2.0" argument.
        """
        mock_get_json.side_effect = [
                Mock(json=Mock(return_value=fixtures.org_payload)),
                Mock(json=Mock(return_value=fixtures.repos_payload))
        ]

        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")

        self.assertEqual(result, fixtures.apache2_repos)
        mock_get_json.assert_called_with("https://api.github.com/orgs/google")
        mock_get_json.assert_called_with(
                "https://api.github.com/orgs/google/repos")


if __name__ == "__main__":
    unittest.main()
