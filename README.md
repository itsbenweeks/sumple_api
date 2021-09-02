sumple_api
----------

A package that contains a simple api that will calculate the sum of post body
values over the past hour.

# Setup

This package was written using Python 3.9. You can either install this package to start 
using this toy API, or you can clone this repository to run tests and develop more features. 

## Install

To install this package, you can run the following command with pip: 
```sh
pip install git+https://github.com/itsbenweeks/sumple_api
```

## Development

To develop this package, clone this repo, and then from the repository's root
and then install the package in editable mode with test dependencies:
```sh
pip install -e ".[test]"
```

### Testing

You can run the testing suite by running `tox` from the command line.

# Running Sumple API
Once you have setup Sumple API, you can run it from your terminal with the
following command: 
```sh
sumple_api
```

## PostMan Collection
If you use [PostMan](https://www.postman.com/downloads/) then you can import a
collection to use against this API. The file to import is located at
`postman/sumple_api.postman_collection.json`.
