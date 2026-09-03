import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 13 Web Services

    Web Services and APIs (Application Programming Interfaces) are your access to the world of data on the internet. While HTTP pages are still great sources of data, increasingly, data are accessed via APIs and your scripts can interact with APIs to get data, publish data, and do all kinds of things.

    ## eXtensible Markup Language - XML
    XML is a more generic markup language than HTML. While HTML is specific to web pages, XML is used for any number of things--it is extensible for any data!

    The example in the text:
    ```xml
    <person>
        <name>Chuck</name>
        <phone type="intl">
         +1 734 303 4456
        </phone>
        <email hide="yes"/>
    </person>
    ```
    XML can be viewed as a tree structure with parent and child nodes.

    Kind of like HTML, we could write parser scripts to parse XML documents. In general, this may be easier than HTML as XML tends to be a bit more strictly defined, but it still a pain--don't do it!
    """)
    return


@app.cell
def _():
    import xml.etree.ElementTree as ET

    data = '''
    <person>
      <name>Chuck</name>
      <phone type="intl">
         +1 734 303 4456
       </phone>
       <email hide="yes"/>
    </person>'''

    tree = ET.fromstring(data)
    print('Name:', tree.find('name').text)
    print('Attr:', tree.find('email').get('hide'))

    # Code: http://www.py4e.com/code3/xml1.py
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## JavaScript Object Notation - JSON

    The JSON format is rapidly growing in popularity, and as noted in the text, has large similarities to Python dictionaries. Here's a JSON:

    ```json
    {
      "name" : "Chuck",
      "phone" : {
        "type" : "intl",
        "number" : "+1 734 303 4456"
       },
       "email" : {
         "hide" : "yes"
       }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And of course there is a json module to use!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Application Programming Interfaces - APIs

    An API is written by a data/service provider as a way for programs to interact with their data/services. Typically, they aren't meant for people to work with directly, but for your scripts to request information and get results back in a parseable format.

    Previous versions of the text covered the Twitter API (now X) and some others, but all now require registration and authentication. This is a common trend as data providers try to monitize their data and services.

    The same has happened with weather data--the last time I taught this course, there were sites with free APIs for getting weather data, most of those have now gone to authenticated only.

    As more and more sites try to monitize thier data, authentication will be more important, and often require payment for access.

    That said, authentication can be a challenge in a course. I do not want to force all of you to sign up for a Google API or some other account. This limits what can be done.

    Luckily, there are still some sites with interesting data and free APIs to access the data...

    I found a nice list of [Public APIs](https://github.com/toddmotto/public-apis) for a wide variety of data.

    And what better data than brery data! Here's the [Open Brewery DB](https://www.openbrewerydb.org/) documentation page.

    Here's an example using the newer `requests` library to access the Open Brewery DB API:
    """)
    return


@app.cell
def _():
    import json
    from typing import Any

    import requests

    SERVICE_URL = 'https://api.openbrewerydb.org/v1/breweries/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    TIMEOUT_SECONDS = 15


    def fetch_breweries_by_city(session: requests.Session, city_name: str) -> list[dict[str, Any]] | None:
        params = {'by_city': city_name}
        print('Retrieving', SERVICE_URL, params)

        try:
            response = session.get(SERVICE_URL, params=params, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            print('Retrieved', len(response.text), 'characters')
            return response.json()
        except requests.exceptions.RequestException as err:
            print('Request error:', err)
            return None
        except ValueError:
            print('Response did not contain valid JSON.')
            return None


    def print_breweries(breweries: list[dict[str, Any]]) -> None:
        print(json.dumps(breweries, indent=4))

        for brewery in breweries:
            print('Brewery name:', brewery.get('name', 'N/A'))
            street = brewery.get('street') or 'N/A'
            city = brewery.get('city') or 'N/A'
            state = brewery.get('state') or 'N/A'
            print('Address:', f'{street}, {city}, {state}')


    def main() -> None:
        session = requests.Session()
        session.headers.update(HEADERS)

        while True:
            city_name = input('Enter a city name to search for breweries (blank to quit): ').strip()
            if not city_name:
                break

            breweries = fetch_breweries_by_city(session, city_name)
            if not breweries:
                print('No brewery data returned.')
                continue

            print_breweries(breweries)


    if __name__ == '__main__':
        main()
    return


if __name__ == "__main__":
    app.run()
