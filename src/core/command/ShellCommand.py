import asyncio

from src.core.utility.Utility import Utility
from src.core.command.base.BaseCommand import BaseCommand

ansi = Utility.colors()


class ShellCommand(BaseCommand):

    helper: dict = {
        'name': 'shell',
        'help': 'This command will allow the user to execute OS shell commands',
        'usage': 'shell <cmd>'
    }

    def __init__(self, command: str, print_queue: asyncio.Queue):
        super().__init__()
        self.command: str = command
        self.print_queue: asyncio.Queue = print_queue

    async def main(self) -> None:
        await self.execute()

    async def execute(self) -> None:
        command = self.command.split(' ')
        command.pop(0)
        await self.run(' '.join(command))

    async def run(self, cmd) -> None:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout:
            await self.print_queue.put('')
            await self.print_queue.put(('success', f"[+] Command: '{cmd}'\n"))
            await self.print_queue.put(stdout.decode())
            await self.print_queue.put(('success', f"[-] Command: '{cmd}'"))
            await self.print_queue.put('')
        if stderr:
            await self.print_queue.put('')
            await self.print_queue.put(('error', f"--=[START CMD: '{cmd}' ]\n"))
            await self.print_queue.put(stderr.decode())
            await self.print_queue.put(('error', f"--=[END CMD: '{cmd}' ]"))
            await self.print_queue.put('')
