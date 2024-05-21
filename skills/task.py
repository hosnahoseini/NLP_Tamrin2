from opsdroid.matchers import match_regex
from opsdroid.skill import Skill
from task.finglish import TextProcessor
from task.data import *
class HelloByeSkill(Skill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_run_once = False
        self.text_processor = TextProcessor(special_words, numbers, two_char, one_char, multiple_char)
    @match_regex(r'.*', case_sensitive=False)
    async def hello(self, message):
        if not self.has_run_once:
            welcome_message = "Welcome to the room! I'm your friendly bot for converting finglish to persian. Send me a finglish text and I will change it to persian"
            await message.respond(welcome_message)
            self.has_run_once = True
        else:
            await message.respond(self.text_processor.run(message.text))
