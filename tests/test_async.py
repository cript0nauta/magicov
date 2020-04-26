import asyncio
from tests.side_effect_utils import c

async def not_called():
    removeme

async def covered_async():
    return 5

asyncio.run(covered_async())

