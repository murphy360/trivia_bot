# The image the tests run in (CI: test-docker) and the image that is published (CI: image).
# The checkout is mounted at /src when the tests run, so the editable install below finds your code there.
FROM python:3.12-slim

WORKDIR /src
COPY pyproject.toml ./
COPY src ./src
# Installs the package and pytest. NEW PROJECT: add your runtime dependencies to pyproject.toml.
RUN pip install --no-cache-dir -e ".[test]"
COPY tests ./tests

# Running the image with no arguments runs the tests. NEW PROJECT: change this to start your service
# once you have one; CI runs the tests with its own command.
CMD ["pytest", "-q"]
