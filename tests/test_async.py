import asyncio
from tests.side_effect_utils import c

async def not_called():
    removeme

async def covered_async():
    return 5

asyncio.run(covered_async())

async def iterator(empty):
    if not empty:
        yield 1
    return

c(1)
async def async_for_empty_list():
    async for _ in iterator(False):
        c(2)
    c(3)
    async for _ in iterator(True):
        removeme

asyncio.run(async_for_empty_list())
