from base64 import b64encode
from os import getenv
from typing import Any, cast

from openai import OpenAI
from streamlit import (
    button,
    cache_resource,
    columns,
    container,
    file_uploader,
    image,
    markdown,
    success,
    text_input,
    warning,
)

with container(border=True):
    markdown("Яке з двох зображень", text_alignment="center")
    question = text_input("питання до двох зображень", label_visibility="collapsed")
    markdown("?", text_alignment="center")

left, right = columns(2)

with left, container(border=True):
    left_file = file_uploader("Перше зображення", "png")

    if left_file:
        image(left_file)

with right, container(border=True):
    right_file = file_uploader("Друге зображення", "png")

    if right_file:
        image(right_file)


@cache_resource
def connect_to_openai():
    return OpenAI(base_url=getenv("ENDPOINT"), api_key=getenv("KEY"))


if button("Запитати", type="primary", width="stretch"):
    if left_file and right_file:
        openai = connect_to_openai()
        image_messages = [
            dict(
                type="image_url",
                image_url=dict(
                    url=f"data:image/png;base64,{b64encode(file.getbuffer()).decode()}"
                ),
            )
            for file in [left_file, right_file]
        ]
        answer = openai.chat.completions.create(
            model="",
            messages=[
                cast(
                    Any,
                    dict(
                        role="user",
                        content=[
                            dict(
                                type="text", text=(f"Яке із двох зображень {question}?")
                            ),
                            *image_messages,
                        ],
                    ),
                )
            ],
        )
        success(answer.choices[0].message.content)
    elif left_file:
        warning("Прикріпіть праве зображення, будь ласка")
    elif right_file:
        warning("Прикріпіть ліве зображення, будь ласка")
    else:
        warning("Прикріпіть зображення, будь ласка")
