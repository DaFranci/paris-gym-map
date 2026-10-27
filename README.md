# Paris Gym Map

Every gym in Paris and Île-de-France on one interactive map. Compare the chains side by side and find the gym closest to your home or your work.

**[Open the map](https://dafranci.github.io/paris-gym-map/)** · available in English and French

## Features

- 600+ gyms across Paris and Île-de-France, grouped by chain (Basic-Fit, Fitness Park, On Air, Neoness, Keepcool…)
- Toggle chains on and off to compare their coverage
- Click any gym for its address, opening hours and website
- Works on desktop and mobile, in light and dark mode

## Data

- Gym locations: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, available under the [Open Database License](https://opendatacommons.org/licenses/odbl/), and the gyms' official websites
- Map tiles: © Esri

Only gyms you can walk into and train at on your own are included. Class-only studios (yoga, pilates, CrossFit, boxing, electrostimulation…), pools and sports clubs are left out.

Spotted a missing, closed or misplaced gym? Please [open an issue](../../issues).

## Running it locally

It's a static site: open `index.html` in a browser. No build step or server needed.

| File | Contents |
|---|---|
| `index.html` | the map |
| `data.js` | gyms from OpenStreetMap |
| `clubs.js` | chain club lists |
| `fetch_gyms.py` | refreshes `data.js` from OpenStreetMap: `python fetch_gyms.py` |
