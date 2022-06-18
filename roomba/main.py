import asyncio
import json
import logging
import time
from roomba import Roomba

if __name__ == '__main__':

    # Uncomment the following two lines to see logging output
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # uncomment the option you want to run, and replace address, blid and roombaPassword with your own values

    address = "192.168.0.132"
    blid = "EEB15740BF3548A982C6BF99A916979C"
    roombaPassword = ":1:1653325360:nzUEQFIwZWTLn0t8"

    myroomba = Roomba(address, blid, roombaPassword)


    # myroomba = Roomba(address) #if you have a config file - will attempt discovery if you don't

    async def test():
        myroomba.connect()
        await asyncio.sleep(10)
        myroomba.set_preference("carpetBoost", "true")
        myroomba.set_preference("twoPass", "false")

        myroomba.send_command("start")
        await asyncio.sleep(30)
        myroomba.send_command("stop")
        await asyncio.sleep(30)
        myroomba.send_command("dock")

        import json, time
        for i in range(10):
            print(json.dumps(myroomba.master_state, indent=2))
            await asyncio.sleep(1)
        myroomba.disconnect()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
