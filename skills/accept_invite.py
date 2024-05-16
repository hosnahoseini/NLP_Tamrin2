
from opsdroid.matchers import match_event
from opsdroid.skill import Skill
from opsdroid.events import UserInvite, JoinRoom, Message
import asyncio
class AcceptInvite(Skill):

    @match_event(UserInvite)
    async def user_invite(self, invite):
        print("USER INVITE")
        if isinstance(invite, UserInvite):
            await invite.respond(JoinRoom())
            # await invite.respond("WELCOME")

            