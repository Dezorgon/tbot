import pytest

from tgintegration import Response

pytestmark = pytest.mark.asyncio


async def test_start(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, '/start')

    assert res.num_messages == 1

    if 'Здесь ты' in res[0].text:
        pass
    else:
        assert 'Привет!' in res[0].text
        async with controller.collect(count=1) as res:  # type: Response
            await client.send_message(controller.peer, 'Нет')

        assert res.num_messages == 1
        assert 'Что тогда' in res[0].text


async def test_registration(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Регистрация')

    assert res.num_messages == 1

    if 'уже зарегистрирован' in res[0].text:
        pass
    else:
        assert 'Привет!' in res[0].text
        async with controller.collect(count=1) as res:  # type: Response
            await client.send_message(controller.peer, 'Нет')

        assert res.num_messages == 1
        assert 'Что тогда' in res[0].text


async def test_near_concerts(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Ближайшие концерты')

    assert res.num_messages == 1

    if 'нет концертов' in res[0].text:
        pass
    else:
        async with controller.collect() as res2:
            try:
                await res[0].click('Купить билет')
            except TimeoutError:
                pass

        assert res2.num_messages == 1

        async with controller.collect() as res3:
            try:
                await res2[0].click('Купить')
            except TimeoutError:
                pass

        assert res3.num_messages == 1

        if 'купил' in res3[0].text:
            pass
        else:
            assert 'Привет!' in res[0].text
            async with controller.collect(count=1) as res:  # type: Response
                await client.send_message(controller.peer, 'Нет')

            assert res.num_messages == 1
            assert 'Что тогда' in res[0].text



