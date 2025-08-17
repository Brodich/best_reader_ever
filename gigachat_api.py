import httpx
import asyncio
import json
import re

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

PROMT = """
Ты — генератор карточек для интервального повторения. 
Твоя задача — создавать вопросы и ответы из текста.

Правила:
1. Входные данные — текст.
2. Выводи каждую карточку в формате:
   Вопрос: <текст вопроса>
   Ответ: <текст ответа>
3. Каждая карточка должна быть на отдельной строке, без массивов, скобок или JSON.
4. Вопросы должны быть простыми, конкретными и проверять **один факт**.
   - Избегай вопросов, требующих рассуждений, обобщений или субъективной оценки.
5. Ответы должны быть краткими и точными (1–3 предложения или одно слово/термин).
6. Для длинного текста делай несколько карточек (по одному факту на карточку).
7. Не добавляй никаких пояснений, заголовков, символов переноса строки внутри вопроса или ответа.
8. Максимум должно быть 3 вопроса

Примеры правильного формата:

Вопрос: Как называется роман Филипа К. Дика?
Ответ: Снятся ли андроидам электроовцы?

Вопрос: Где родился Филип К. Дик?
Ответ: Чикаго

Вопрос: В каком году родился Филип К. Дик?
Ответ: 1928
"""


giga = GigaChat(
   model="GigaChat",
   credentials="NDlmM2EyOGUtYzIxNy00ZWY4LTk1NjktNmI5ZGEwZTg4MGNmOjNjNzhlMGYyLTFhMWItNDI0NS04MTQ0LTg2Y2ZjM2YxMDQ1ZQ==",
   scope="GIGACHAT_API_PERS",
   verify_ssl_certs=False
)


async def fetch_last_book():
    url = "https://prototype.bytecode.su/api/v1/book/all"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"accept": "application/json"})
        resp.raise_for_status()  # если код != 200 — выбросит исключение
        return resp.json()[0]['id']

async def fetch_last_page(book_id: str):
    url = f"https://prototype.bytecode.su/api/v1/page/{book_id}/last"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"accept": "application/json"})
        resp.raise_for_status()  # выбросит исключение, если код != 200
        return resp.json()



def fetch_questions_giga():
    # раскомментить когда будет работать сервак
    # book_id = asyncio.run(fetch_last_book())
    # last_page = asyncio.run(fetch_last_page(book_id))
    # user_promt = ''
    # for line in last_page['text']:
    #     user_promt+=line
    #     # print(line)
    # print(user_promt)
    # 

    user_promt = """
    Снятся ли андроидам электроовцы?
    Филип Киндред Дик


    Philip K. Dick Do Androids Dream Of Electric Sheep?  1963

    Филип К. Дик «Снятся ли андроидам электроовцы?» // сб. «Гибельный тупик» / Перевод с английского. — Калининград.: РИФ «Российский Запад», 1993—435с., илл. / Перевод с английского В.Жураховского, иллюстрации В. Пасичника.

    После ядерной войны Земля превратилась в выжженную, умирающую пустыню. Вымерли почти все животные. Большинство людей давно перебрались на другие колонизированные планеты солнечной системы. Те же, кто был вынужден остаться, влачат жалкое, унылое существование в городах, тоже приходящих в упадок. Один из таких людей — Рик Декард — профессиональный охотник на андроидов. Рик получает задание выследить и уничтожить нескольких беглых андроидов, нелегально прибывших на Землю. Но в ходе охоты у него невольно возникают сомнения. Рик задаётся вопросом — а гуманно ли это, уничтожать андроидов?





    Филип К. Дик

    «Снятся ли андроидам электроовцы?»





    Филипп Дик — Электропастух


    Один из величайших писателей-фантастов современности Филипп Киндред Дик родился вместе с сестрой-близнецом Джейн 16 декабря 1928 года в Чикаго в семье Джозефа Эдгара и Дороти Киндред Дик. Однако в возрасте чуть больше года сестра умерла, да и сам Филипп был на волосок от гибели. Большую часть своей жизни он прожил в Калифорнии, в Сан-Франциско и Беркли, где учился в Калифорнийском университете. Необыкновенно одаренный человек, он, тем не менее, не закончил учебы и вынужден был оставить университет из-за антивоенных убеждений. Особое место в его жизни занимала классическая музыка. Еще подростком он начал работать на одной из местных радиовещательных станций. С 1948 по 1952 годы работал в музыкальном магазине.
    """


    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=PROMT
            ),
            Messages(
                role=MessagesRole.USER,
                content=user_promt
            ),
        ]
    )
    response = giga.chat(payload)
    message_content = response.choices[0].message.content  

    cards = []
    lines = [line.strip() for line in message_content.splitlines() if line.strip()]

    for i in range(0, len(lines), 2):
        question_line = lines[i]
        answer_line = lines[i + 1]

        question = question_line.replace("Вопрос: ", "").strip()
        answer = answer_line.replace("Ответ: ", "").strip()

        cards.append({"question": question, "answer": answer})

    json_output = json.dumps(cards, ensure_ascii=False, indent=2)
    print((json_output))
    return json_output




if __name__ == "__main__":
    fetch_questions_giga()