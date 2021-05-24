import pytest

from tgintegration import Response

pytestmark = pytest.mark.asyncio


async def test_start(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, '/start')

    assert res.num_messages == 1

    assert 'Смотрю ты новенький' in res[0].text
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Нет')

    assert res.num_messages == 1
    assert 'Что тогда' in res[0].text


async def test_registration(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Регистрация')

    assert res.num_messages == 1

    assert 'Смотрю ты новенький' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Да')
    assert res.num_messages == 1
    assert 'с имени' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'не Конь')
    assert res.num_messages == 1
    assert 'Фамилия' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'не Боцык')
    assert res.num_messages == 1
    assert 'дату своего рождения' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'не дата')
    assert 'Введи дату' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Перехотелось')
    assert 'Ну и ладно' in res[0].text


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
        assert 'Привет!' in res3[0].text
        await register_dialog(controller, client)


async def register_dialog(controller, client):
    res = await input_registration_data(controller, client)

    async with controller.collect() as res2:
        try:
            await res[0].click('Давай по новой Миша')
        except TimeoutError:
            pass
    assert 'Привет!' in res2[0].text

    res = await input_registration_data(controller, client)

    async with controller.collect() as res2:
        try:
            await res[0].click('Норм')
        except TimeoutError:
            pass
    assert 'Ок' in res2[0].text


async def input_registration_data(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Да')
    assert res.num_messages == 1
    assert 'с имени' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Конь')
    assert res.num_messages == 1
    assert 'Фамилия' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Боцык')
    assert res.num_messages == 1
    assert 'дату своего рождения' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'не дата')
    assert 'Введи дату' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, '23.04.1999')
    assert 'Конь Боцык 23.04.1999' in res[0].text

    return res


async def test_concerts_by_city(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Посмотреть концерты в моем городе')
    assert res.num_messages == 1
    assert 'В каком городе' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Ыблымск')
    assert res.num_messages == 1
    assert 'не нашел концертов' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Посмотреть концерты в моем городе')
    assert res.num_messages == 1
    assert 'В каком городе' in res[0].text

    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Минск')
    assert res.num_messages == 1

    async with controller.collect() as res2:
        try:
            await res[0].click('Купить билет')
        except TimeoutError:
            pass

    assert res2.num_messages == 1

    async with controller.collect() as res3:
        try:
            await res2[0].click('>')
        except TimeoutError:
            pass
        try:
            await res2[0].click('Купить')
        except TimeoutError:
            pass

    assert res3.num_messages == 3
    assert 'Ну купил ты билет' in res3[2].text


async def test_profile(controller, client):
    async with controller.collect(count=1) as res:  # type: Response
        await client.send_message(controller.peer, 'Профиль')

    assert res.num_messages == 1
    assert 'Билеты' in res[0].text
