from logging import Logger, getLogger

import requests

import settings_back


class Client:
    BASE_URL: str = "https://api.themoviedb.org"
    API_VERSION: str = "3"

    _logger: Logger = None
    _token: str = None

    def __init__(self, logger: Logger = getLogger(__name__)):
        self._logger = logger
        self._token = settings_back.MOVIE_DB_TOKEN

    def _request(self, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params["language"] = "fr-FR"

        response = requests.get(
            url=f"{self.BASE_URL}/{self.API_VERSION}/{endpoint}",
            params=params,
            headers={"Authorization": f"Bearer {self._token}"},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 401:
                self._logger.error("Unauthorized request")
            elif response.status_code == 429:
                self._logger.error(f"Rate limit exceeded: {response.content}")

            raise e

        return response.json()

    def get_trending_movies(self) -> dict:
        return self._request(
            endpoint="trending/movie/week",
        )

    def get_movie_by_title(self, title: str) -> dict:
        return self._request(
            endpoint="search/movie",
            params={"query": title},
        )

    def get_movie_by_id(self, movie_id: int) -> dict:
        return self._request(
            endpoint=f"movie/{movie_id}",
        )

    def get_movie_credits(self, movie_id: int) -> dict:
        return self._request(
            endpoint=f"movie/{movie_id}/credits",
        )

    def get_person_by_id(self, person_id: int) -> dict:
        return self._request(
            endpoint=f"person/{person_id}",
        )

    def get_person_by_name(self, name: str) -> dict:
        return self._request(
            endpoint="search/person",
            params={"query": name},
        )
