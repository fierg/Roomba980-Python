import asyncio
import logging
import pigpio
from starlette import status

from roomba import Roomba
from fastapi import FastAPI

app = FastAPI(title="Roomba Control", description="Control Romba over RESTApi", version="0.0.1")
STATE = 0
GREEN = 22
RED = 17
iteration = 0


@app.get("/run", status_code=status.HTTP_201_CREATED)
async def _get_run():
    global STATE
    STATE = 1

    return


@app.get("/stop", status_code=status.HTTP_200_OK)
async def _get_stop():
    global STATE
    STATE = 2

    return


async def run():
    await init()
    global STATE
    global iteration

    while STATE != -1:
        iteration += 1
        logging.info(f'current event loop state: {STATE}')

        if STATE == 1:
            await start()
        elif STATE == 2:
            await stop()
        elif STATE == 3:
            await dock()
        else:
            for i in range(2):
                # print(json.dumps(roomba.master_state, indent=2))
                await asyncio.sleep(1)

        if iteration == 5:
            STATE = STATE + 1
            iteration = 0

    roomba.disconnect()
    pi.stop()


async def dock():
    await asyncio.sleep(30)
    roomba.send_command("dock")
    global STATE
    STATE = -1


async def start():
    roomba.send_command("start")
    pi.set_PWM_dutycycle(GREEN, 255)
    await asyncio.sleep(30)
    global STATE


async def init():
    roomba.connect()
    await asyncio.sleep(5)
    roomba.set_preference("carpetBoost", "true")
    roomba.set_preference("twoPass", "true")
    await asyncio.sleep(5)


async def stop():
    global STATE

    pi.set_PWM_dutycycle(GREEN, 0)
    pi.set_PWM_dutycycle(RED, 255)

    await asyncio.sleep(5)

    roomba.send_command("stop")

    await asyncio.sleep(30)


def button_callback():
    logging.info("Button was pushed!")
    global STATE
    STATE = 2


def main():
    global roomba
    global pi
    button_pin = 26

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # replace address, blid and roombaPassword with your own values
    address = "192.168.0.132"
    blid = "EEB15740BF3548A982C6BF99A916979C"
    roombaPassword = ":1:1653325360:nzUEQFIwZWTLn0t8"

    # myroomba = Roomba(address) #if you have a config file - will attempt discovery if you don't
    roomba = Roomba(address, blid, roombaPassword)

    pi = pigpio.pi()
    pi.set_mode(button_pin, pigpio.INPUT)
    pi.callback(button_pin, pigpio.FALLING_EDGE, button_callback)

    loop = asyncio.get_event_loop()
    loop.create_task(run())

    try:
        loop.run_forever()

    except (KeyboardInterrupt, SystemExit):
        logging.info("System exit Received - Exiting program")
        roomba.disconnect()
        logging.info('Program Exited')

    finally:
        pass


if __name__ == '__main__':
    main()
