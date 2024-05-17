from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from datetime import datetime, date


@hook(priority=3)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    if "prompt_settings" in user_message_json:
        cat.working_memory["lang"] = user_message_json["prompt_settings"]["lang"]
        cat.working_memory["translate"] = user_message_json["prompt_settings"].get(
            "translate", False
        )
    return user_message_json


@hook(priority=1)
def agent_fast_reply(fast_reply, cat):
    if cat.working_memory["translate"]:
        user_message = cat.working_memory["user_message_json"]["text"]
        lang = cat.working_memory["lang"]
        prompt= f"""Your job is to tanslate the following phrase from the user into the language requested.
### Examples
user: oggi ho mangiato la pasta
lang: English
ai: today i ate pasta

user: oggi ho mangiato la pasta
lang: Spanish
ai: hoy he comido pasta

### Input
user: {user_message}
lang: {lang}
ai:"""
        translation = cat.llm(prompt)
        fast_reply = {
            "output": translation
        }
        

    return fast_reply
