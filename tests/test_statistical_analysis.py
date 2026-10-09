
import unittest
import pandas as pd

from utils.statistical_analysis import (
    groupwise_analysis,
    highest_group_average,
    lowest_group_average,
    category_counts,
    numerical_summary,
)


class TestStatisticalAnalysis(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "school": ["A", "A", "B", "B"],
            "sex": ["F", "M", "F", "M"],
            "G3": [10, 12, 14, 16],
            "absences": [2, 4, 6, 8],
        })

    def test_groupwise_average(self):
        result = groupwise_analysis(
            self.df, "school", "G3"
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

        school_a = result[
            result["school"] == "A"
        ]["mean"].iloc[0]

        self.assertEqual(school_a, 11.0)

    def test_highest_group_average(self):
        result = highest_group_average(
            self.df, "school", "G3"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["group"], "B")
        self.assertEqual(result["value"], 15.0)

    def test_lowest_group_average(self):
        result = lowest_group_average(
            self.df, "school", "G3"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["group"], "A")
        self.assertEqual(result["value"], 11.0)

    def test_invalid_column(self):
        result = groupwise_analysis(
            self.df, "unknown", "G3"
        )

        self.assertIsNone(result)

    def test_category_counts(self):
        result = category_counts(
            self.df, "school"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["Count"].sum(), 4)

    def test_numerical_summary(self):
        result = numerical_summary(self.df)

        self.assertIsNotNone(result)
        self.assertIn("G3", result["Column"].tolist())


if __name__ == "__main__":
    unittest.main()