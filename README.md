# Crosschq Backend Developer Challenge

## Installing process and Notes

This project is intented to be run with python 3.

* install _pipenv_ (https://docs.pipenv.org/en/latest/)
* clone this repo.
* and then run

```
cd {cloned-repo-directory}
pipenv install
make migrate
```

* check the Makefile, it contains some useful commands/helpers

to run the import script run

```
make import_books
```

* to clean the database just remove the sqlite file and run migrate again

## Tasks

* Fix the import_books script.
* write a test for the import_books script
* write a rest endpoint that will let you list and search the books
  * DRF is configured in the project already
  * limit the endpoint to allow only to get information for non-logged users
  * must required authentication to create / edit/ delete books through the api
* improve the admin adding search and filters
