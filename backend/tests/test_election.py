import pytest

from httpx import AsyncClient
from fastapi import FastAPI


from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY


from app.models.election import  PartyModel,ConstituencyModel

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_constituency():
    return ConstituencyModel(name="Reading", votesdata={}, winnervotes=3, winnerparty="L")



class TestConstituencyRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("constituencies:get-constituency-by-name"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("constituencies:get-constituency-by-name"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestGetConstituency:
    async def test_get_constituency_by_name(self, app: FastAPI, client: AsyncClient, test_constituency: ConstituencyModel) -> None:
        res = await client.get(app.url_path_for("constituencies:get-constituency-by-name", id=test_constituency.id))
        assert res.status_code == HTTP_200_OK
        constituency = ConstituencyModel(**res.json())
        assert constituency == test_constituency

    @pytest.mark.parametrize(
        "id, status_code", ((500, 404), (-1, 404), (None, 422),),
    )
    async def test_wrong_id_returns_error(self, app: FastAPI, client: AsyncClient, id: int, status_code: int) -> None:
        res = await client.get(app.url_path_for("constituencies:get-constituency-by-name", id=id))
        assert res.status_code == status_code

