from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
from task.run import run
class PhinglishSkill(Skill):
    @match_regex(r'.*')
    async def say_hi(self, message):
        await message.respond(run(message.text))
