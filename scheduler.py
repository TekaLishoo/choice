from rocketry import Rocketry
from rocketry.conds import every
from dress.update_dresses import update_dresses


app = Rocketry()


@app.task("daily")
async def do_things():
    """
    Daily dresses update in database.
    """
    # pass
    await update_dresses()
