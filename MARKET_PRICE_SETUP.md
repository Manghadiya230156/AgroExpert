# AgroExpert Market Price Insights setup

## Official data source
The page uses the data.gov.in Current Daily Price of Various Commodities from Various Markets (Mandi) resource. Only official returned prices are displayed; missing prices are not fabricated. The API's reporting coverage varies by state, district, commodity and date. A broader date filter cannot recover rows the API does not return.

## Configure the API key (Windows CMD)
Run this in the same CMD window used to start Django:

```bat
set "DATA_GOV_IN_API_KEY=YOUR_REGENERATED_API_KEY"
cd agroexpert_backend
python manage.py migrate
python manage.py check
python manage.py runserver
```

In PowerShell use `$env:DATA_GOV_IN_API_KEY="YOUR_REGENERATED_API_KEY"` instead. Never commit the real key or include it in a ZIP. If a key was exposed in a screenshot, regenerate it.

## Market filters
- State is a dropdown containing all Indian states and union territories. Gujarat is selected by default.
- District depends on the selected state. Gujarat and Punjab use local district lists; other states use distinct districts returned by the official market-price feed. This means the fallback list represents districts with currently available price records, not necessarily every administrative district.
- The market/mandi text field was removed.
- Commodity is intentionally a text filter so users can search any commodity published by the source (including cotton, groundnut, rice, wheat, pulses, spices, fruits and vegetables). Leave it blank to fetch all commodities available for the selected location.
- Pagination follows the API `total` field and is capped at 20,000 records per request for safety. Narrow state/district/commodity filters if the API total exceeds this cap.

## Database
Run `python manage.py migrate` after updating the code. Back up `db.sqlite3` before replacing or migrating a database. Existing `MarketPriceSnapshot` data is cached for six hours; cached records may be older than the newest government report.

## Notes
The Django development server is for local development only. Before deployment, set a strong `SECRET_KEY`, `DEBUG=False`, and explicit `ALLOWED_HOSTS`, and configure a production database and HTTPS.
