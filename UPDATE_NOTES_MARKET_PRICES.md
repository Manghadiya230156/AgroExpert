# Market Price Insights update notes

Implemented in this package:

- State dropdown contains all Indian states and union territories, with Gujarat selected by default.
- District dropdown changes when the state changes. Gujarat and Punjab use district lists bundled in the project; for other states the list is built from districts present in the official market-price feed.
- Removed the manual Market/Mandi input.
- Kept the commodity filter open-ended, so users can query any commodity published by AGMARKNET (cotton, groundnut, rice, wheat, pulses, spices, fruits, vegetables, etc.). No crop-category restriction is applied by the view.
- Added Market Price Insights to the farmer dashboard, retaining existing cards.
- Added API pagination (up to 20,000 records per filter set), response validation, normalized records and clear cache/error messaging.
- Added the MarketPriceSnapshot table to the included SQLite database because the bundled database had migrations through 0008 but did not yet have the 0009 cache table.
- Added `setup_windows.bat` to run database migrations and Django checks before starting the local development server.
- Replaced wildcard allowed hosts and the committed Django secret key with environment-based settings and local-development defaults.

## Validation status

Python source compilation and JavaScript syntax checks passed in the packaging environment. A full Django `manage.py check` could not be executed here because Django is not installed in the packaging environment and network access is unavailable to install it. Run `python manage.py migrate` and `python manage.py check` in the project's configured Python environment before deployment.

## Data coverage limitation

The app only displays records returned by the official data.gov.in API. If the source reports 59 Gujarat records for a given query, this code cannot create additional real price observations. Pagination fetches additional pages when the API reports them. District options for states other than Gujarat and Punjab are based on districts with records in the current feed; the live price feed is not a complete administrative-district registry. The source may publish a limited current-day selection, and date filters cannot create historical records that the source did not return.
