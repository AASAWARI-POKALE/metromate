# MetroMate – Smart & Accessible Metro Navigator

MetroMate is a student-built prototype that helps metro passengers find an indoor station route based on their needs. The same destination can have different recommended routes for different passengers.

## Problem statement

Large metro stations can be confusing for first-time passengers. A single set of arrows cannot serve everyone equally. A wheelchair user may need a step-free route using lifts, a passenger in a hurry may prefer a faster escalator route, and another passenger may prefer stairs.

## Features

- Personalised routing for wheelchair / step-free, fastest, stairs-preferred and luggage preferences.
- Flask REST API that calculates routes using Dijkstra's shortest-path algorithm.
- Demo station graph containing entrances, concourses, lifts, stairs, escalators and platforms.
- English, Hindi and Marathi interface.
- Responsive frontend for desktop and mobile.
- Clear step-by-step route instructions and illustrative travel times.

## Tech stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Routing: weighted graph + Dijkstra's algorithm
- Data: JSON (easy to replace with real station data later)

## Run locally on Windows

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Open Terminal → New Terminal.
5. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:

   ```cmd
   .venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Start the server:

   ```bash
   python app.py
   ```

8. Open http://127.0.0.1:5000 in your browser.

## API endpoints

### `GET /api/health`

Checks whether the backend is running.

### `GET /api/station`

Returns the station name, navigation nodes and connections.

### `POST /api/route`

Example request:

```json
{
  "start": "gate_a",
  "end": "platform_1",
  "preference": "wheelchair"
}
```

Supported preferences: `wheelchair`, `hurry`, `stairs`, `luggage`.

## Project structure

```text
metromate/
├── app.py
├── data/
│   └── station.json
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```

## Important limitations

This is a learning prototype with fictional station data and illustrative travel times. It is not intended for real-world navigation. A production system would need verified station maps, live lift/escalator status, platform changes, emergency exits, accessibility audits, multilingual content review and testing with passengers with disabilities. Never rely on this demo for safety-critical directions.

## Future improvements

- Add multiple stations and inter-station journey planning.
- Import verified station maps and model each floor separately.
- Add live lift/escalator outage alerts.
- Add QR codes at station entry points to set the passenger's current location.
- Add voice guidance and text-to-speech.
- Add administrator dashboard to update station layout.
- Add unit tests and accessibility testing.
- Add a map view with floor-by-floor visual directions.

## Suggested first GitHub issues

1. Add a visual station map.
2. Add voice navigation.
3. Add a Hindi/Marathi translation review.
4. Add automated tests for wheelchair-safe routes.
5. Add a station editor for administrators.

## Contribution

Pull requests are welcome. For changes to route logic, include a test case showing why the route is suitable for the selected passenger preference.
