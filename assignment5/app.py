"""
strompris fastapi app entrypoint
"""
import datetime
from pathlib import Path
from typing import Annotated

import altair as alt
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import (
    BaseModel,
)  # importert for egen metode, htmlresponse er importert for 5.2

from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date


EARLIEST_DATE = datetime.date.today() - datetime.timedelta(days=60)


@app.get("/")
def home(request: Request):
    """entry point for home screen. should display a chart with some options for
    selecting what kind of infomration you want to display

    Parametres: request: Request -- a request

    Returns:
        a templateresponse
    """
    today = datetime.date.today()
    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "today": today,
            "days": 7,
        },
    )




# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)


# locations: Annotated[dict[str, str] | None, Query()] = None,
@app.get("/plot_prices.json")
def plot_prices_json(
    request: Request,
    locations: Annotated[list[str] | None, Query()] = list(LOCATION_CODES.keys()),
    end: Annotated[datetime.date | None, Query()] = datetime.date.today(),
    days: Annotated[int | None, Query()] = 7,
) -> dict:
    """
    Method that generates a json chart (alt.chart.to_dict()) from by drawing on the fetch_prices method in strompris.py.
    I've included some limitations in order to make sure that the user will not request more data than what the app can handle,
    (currently 30 days)
    as well as not trying to access data that is earlier than today's date minus 60 days.

    Parameters:
        request: a http request
        locations: the location codes that you want to collect data from
        end: the final day to collect data for. should be no earlier than todays date - 60 days
        days: number of data to collect data for, max = 30


    """
    if end is not None and end > datetime.date.today():
        raise HTTPException(
            status_code=400,
            detail="Invalid end date. You cannot select an end date that is later than today",
        )

    if EARLIEST_DATE > end:
        raise HTTPException(
            status_code=400,
            detail="Invalid end date. You cannot select an end date that is earlier than today's date minus 60 days",
        )

    if locations is None:
        raise HTTPException(status_code=400, detail="No locations selected!")

    if days != None and (days > 30 or type(days) != int):
        raise HTTPException(
            status_code=400,
            detail="You have either entered something that is not an integer or entered too many days. Our servers are old and tired",
        )
    df = fetch_prices(end, days, locations)
    chart = plot_prices(df)
    return chart.to_dict()


# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


...


# mount your docs directory as static files at `/help`


app.mount(
    "/help",
    app=StaticFiles(
        directory=Path(__file__).parent / "docs" / "_build" / "html", html=True
    ),
    name="help",
)


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
