from django.test import TestCase

from home.metrics import Metrics


class MetricsTestCase(TestCase):
    os_metrics = [
        {"operating_systems": "windows", "year": 2014, "count": 32},
        {"operating_systems": "linux", "year": 2014, "count": 8},
        {"operating_systems": "platform_independent", "year": 2014, "count": 55},
        {"operating_systems": "macos", "year": 2014, "count": 8},
        {"operating_systems": "linux", "year": 2015, "count": 6},
        {"operating_systems": "platform_independent", "year": 2015, "count": 60},
        {"operating_systems": "windows", "year": 2015, "count": 28},
        {"operating_systems": "macos", "year": 2015, "count": 19},
        {"operating_systems": "other", "year": 2017, "count": 1},
        {"operating_systems": "linux", "year": 2017, "count": 4},
        {"operating_systems": "windows", "year": 2017, "count": 67},
        {"operating_systems": "macos", "year": 2017, "count": 21},
        {"operating_systems": "platform_independent", "year": 2017, "count": 37},
        {"operating_systems": "platform_independent", "year": 2018, "count": 56},
        {"operating_systems": "other", "year": 2018, "count": 1},
        {"operating_systems": "linux", "year": 2018, "count": 3},
        {"operating_systems": "macos", "year": 2018, "count": 18},
        {"operating_systems": "windows", "year": 2018, "count": 54},
        {"operating_systems": "", "year": 2018, "count": 9},
    ]

    def test_convert_timeseries(self):
        """
        exercise the conversion of timeseries data by category that fills in years
        Metrics.convert_codebase_metrics_to_timeseries
        """
        m = Metrics()
        min_start_year = 2012
        OS_NAMES = ("linux", "other", "platform_independent", "windows", "macos")
        highcharts_timeseries = m.convert_release_metrics_to_timeseries(
            self.os_metrics, start_year=min_start_year
        )
        for chart_data in highcharts_timeseries:
            # 2012 and 2013 should also be 0
            self.assertEquals(
                tuple(chart_data["data"][0:2]),
                (0, 0),
                "2012-13 should be zeroed out",
            )
            # missing year 2016
            self.assertEquals(
                chart_data["data"][4],
                0,
                f"5th entry (2016) should be 0 {chart_data['name']}",
            )
            self.assertTrue(
                chart_data["name"] in OS_NAMES, f"Invalid OS name {chart_data['name']}"
            )
            self.assertEquals(len(chart_data["data"]), 7, "Should be 7 years of data")
