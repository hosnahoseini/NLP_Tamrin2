from opsdroid.matchers import match_regex
from opsdroid.skill import Skill
from task.run import run

class HelloByeSkill(Skill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_run_once = False

    @match_regex(r'hi|hello|hey|hallo', case_sensitive=False)
    async def hello(self, message):
        if not self.has_run_once:
            welcome_message = "Welcome to the room! I'm your friendly bot for converting finglish to persian. Send me a finglish text and I will change it to persian"
            await message.respond(welcome_message)
            self.has_run_once = True
        else:
            await message.respond(run(message.text))
