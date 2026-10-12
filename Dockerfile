# The image the tests run in (CI: test-docker) and the image that is published (CI: image).
# The checkout is mounted at /src when the tests run, so the editable install below finds your code there.
FROM python:3.14-slim

WORKDIR /src
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[test]"
COPY tests ./tests

# The bot runs as an unprivileged user and keeps its database in /data.
RUN useradd --uid 1000 --create-home bot && mkdir /data && chown bot:bot /data
VOLUME /data
USER bot

# CI runs the tests with its own command (pytest -q).
CMD ["python", "-m", "trivia_bot"]
