from reports.tests.test_setup import TestReportSetup
from rest_framework import status
from datetime import date
from decimal import Decimal


class TestReportAPI(TestReportSetup):
    def test_get_all_reports(self):
        response = self.client.get("/api/v1/reports/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_report_filtered_by_restaurant(self):
        response = self.client.get("/api/v1/reports/?restaurant=Restaurant_A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 3)
        for report in response.data:
            self.assertEqual(report.get("restaurant"), "Restaurant_A")

    def test_get_report_filtered_by_date_range(self):
        start_date = date(2023, 4, 1)
        end_date = date(2024, 5, 22)
        response = self.client.get(
            f"/api/v1/reports/?date__gte={start_date.isoformat()}&date__lte={end_date.isoformat()}"
        )

        self.assertEqual(len(response.data), 2)

        for report in response.data:
            resp_date = date.fromisoformat(report.get("date"))
            self.assertLess(resp_date, end_date)
            self.assertGreater(resp_date, start_date)

    def test_get_report_sorted_by_model_fields(self):
        response = self.client.get("/api/v1/reports/?sort_by=date")
        self.assert_list_sorted_by_asc(response.data, "date")

        response = self.client.get("/api/v1/reports/?sort_by=-date")
        self.assert_list_sorted_by_desc(response.data, "date")

        response = self.client.get("/api/v1/reports/?sort_by=restaurant")
        self.assert_list_sorted_by_asc(response.data, "restaurant")

        response = self.client.get("/api/v1/reports/?sort_by=-restaurant")
        self.assert_list_sorted_by_desc(response.data, "restaurant")

        response = self.client.get(
            "/api/v1/reports/?sort_by=planned_actual_hours_delta"
        )
        self.assert_list_sorted_by_asc(response.data, "planned_actual_hours_delta")

        response = self.client.get(
            "/api/v1/reports/?sort_by=-planned_actual_hours_delta"
        )
        self.assert_list_sorted_by_desc(response.data, "planned_actual_hours_delta")

        response = self.client.get("/api/v1/reports/?sort_by=budget_sells_delta")
        sorted_data = sorted(
            response.data, key=lambda x: float(x["budget_sells_delta"])
        )
        self.assertEqual(response.data, sorted_data)

        response = self.client.get("/api/v1/reports/?sort_by=-budget_sells_delta")
        sorted_data = sorted(
            response.data, key=lambda x: float(x["budget_sells_delta"]), reverse=True
        )
        self.assertEqual(response.data, sorted_data)

    def assert_list_sorted_by_asc(self, list, field):
        sorted_list = sorted(list, key=lambda x: x[field])
        self.assertEqual(list, sorted_list)

    def assert_list_sorted_by_desc(self, list, field):
        sorted_list = sorted(list, key=lambda x: x[field], reverse=True)
        self.assertEqual(list, sorted_list)


class TestAggregateReportAPI(TestReportSetup): ...
