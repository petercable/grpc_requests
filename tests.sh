#!/bin/bash

# Run this script before commits to count the number of flake8 errors and
# and ensure tests are passing.

flake8 . --count  --show-source --statistics

pytest --cov-report=xml --cov=src/grpc_requests