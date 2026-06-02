import nest_asyncio
import asyncio
from src.flappy import Flappy

nest_asyncio.apply()

if __name__ == "__main__":
    asyncio.run(Flappy().start())
    