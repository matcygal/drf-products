# drf-products

[![CircleCI](https://circleci.com/gh/matcygal/drf-products.svg?style=shield)](https://app.circleci.com/pipelines/github/matcygal/drf-products)

Used tech:
Django, DRF, drf_yasg, CircleCI and sqlite

CircleCi is running test at git push

Starting dev:
  > docker-compose up -d

Running tests:
  > docker-compose run alpine sh -c " python manage.py test "
  
All endpoints are documented in Swagger-UI:
  > [Swagger-UI link](http://0.0.0.0:8000/swagger)
