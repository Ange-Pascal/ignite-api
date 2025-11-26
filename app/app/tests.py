"""
Sample tests for the calc module.
"""

from django.test import SimpleTestCase
from app.calc import add


class CalcTests(SimpleTestCase):
    """Test suite for calculator functions."""

    def test_add_numbers(self):
        """Test that two numbers are added correctly."""
        result = add(2, 5)
        self.assertEqual(result, 7)
