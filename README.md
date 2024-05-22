# Python Django Exercise
An exercise for a backend service written in Python with Django that imports data from a csv file to its database,
and exposes this data through a REST api with various features.

## Assignment
The dataset.csv file contains daily reports: 

| date       | restaurant  | planned_hours | actual_hours | budget  | sells   |
|------------|-------------|---------------|--------------|---------|---------|
| 2016-01-01 | Copacabana  | 141           | 176          | 4025.65 | 2801.33 |
| 2016-01-01 | Noodle Bar  | 108           | 76           | 2455.75 | 3875.81 |
| 2016-01-01 | Jack Rabbit | 30            | 156          | 116.99  | 3967.95 |
| 2016-01-02 | Copacabana  | 189           | 135          | 611.8   | 197.57  |
| 2016-01-02 | Noodle Bar  | 136           | 205          | 684.13  | 1720.22 |
| ...        | ...         | ...           | ...          | ...     | ...     |

We want to build an application with Python + Django and complete these assignments:
1) Implement an import procedure for the "dataset.csv" file that can be started at any time with a command.
2) Calculate the difference between `planned_hours` and `actual_hours`, and between budget and sells.
3) Develop a REST API that exposes the imported data.
4) Implement a filtering functionality for the `restaurant` field.
5) Implement data grouping by `date` and `restaurant`, applying the SQL aggregation function *SUM*.
6) Add filtering for date ranges (`date__lte`, `date__gte`).
7) Implement sorting for each available field, including calculated deltas, in both ascending and descending order.
8) Write automated tests to verify the functionality and robustness of the API.

## Solution
The project contains a single application called `reports`.
1) The import procedure is defined with a Django command in `reports/management/commands/import_reports.py`. The procedure is also tested in `reports/tests/test_import_reports.py`.
2) The deltas are defined as django `GeneratedField` in the Report model (`reports/models.py`), which are calculated automatically whenever the object is written in the database. This allows us later on to perform sorting on them easily and efficiently, using the database itself.
3) The REST API is in `reports/views.py`, it is written using two auxiliary libraries: `djangorestframework` and `django-filter`. The views for the GET methods are defined with the rest framework `ListAPIView` class.
4) Filtering is done with the `DjangoFilterBackend`, using a custom filter: `ReportFilter`. This filter allows us to filter by restaurant name.
5) The data grouping API uses a different REST resource called `aggregate-report`, it is possible to filter by restaurant name or date (or both), and the API will return the aggregate report with the sum of all numeric values of the combined reports. The sum is performed via the django `Sum` function on the model queryset, which performs SQL SUM functions under the hood (it can be seen by enabling SQL logging in `settings.py` by uncommenting the LOGGING section).
6) Filtering by date range is also done with the custom filter `ReportFilter`.
7) Sorting is done in `ReportFilter` by defining a `django_filters.OrderingFilter` over the model fields.
8) All tests can be found under the `reports/tests/` directory. There are tests for all API endpoints and for the csv importer.

# Project setup (with make)
Required: python (pyenv suggested), poetry, postgres, docker. (*If you don't want to use make, the original commands can be found in the Makefile.*)
1) activate a venv: `make shell`
2) install deps: `make deps`
3) start the database: `make up`
4) execute migrations: `make db-migrate`
5) run the tests: `make test`

# Run the project
1) Import the records from `dataset.csv`: `python manage.py import_reports` (optionally, a different filename can be passed as argument)
2) Run the server: `make run`
With the server up and running, we can try out its APIs.

## Available APIs
*Note: All query params can be stringed together for a combined query.*

### Reports
- `GET /api/v1/reports/` - list all reports
- `GET /api/v1/reports/?restaurant=name` - list all reports filtered by restaurant name
- `GET /api/v1/reports/?date__gte=YYYY-MM-DD&date__lte=YYYY-MM-DD` - list all reports in a date range
- `GET /api/v1/reports/?sort_by=field` - list all reports sorted by field

### Aggregate report
- `GET /api/v1/aggregate-report/?date=YYYY-MM-DD` - get a combined report by date
- `GET /api/v1/aggregate-report/?restaurant=name` - get a combined report by restaurant name
(*It is also possible to filter by both, but not very useful given the dataset*)
