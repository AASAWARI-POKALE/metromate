from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
import heapq

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "station.json"

def load_station():
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)

def edge_cost(edge, preference):
    """Return the preference-aware cost of using an edge."""
    kind = edge["type"]
    minutes = edge["minutes"]

    if preference == "wheelchair":
        # Wheelchair routes must be step-free. Escalators are excluded too.
        if kind in ("stairs", "escalator"):
            return None
        return minutes

    if preference == "luggage":
        # Avoid stairs where possible, but allow them if there is no alternative.
        return minutes + (18 if kind == "stairs" else 0) + (2 if kind == "escalator" else 0)

    if preference == "stairs":
        return minutes + (0 if kind == "stairs" else 5)

    if preference == "hurry":
        # The sample times already represent estimated traversal time.
        return minutes

    return minutes

def find_route(station, start_id, end_id, preference):
    nodes = {node["id"]: node for node in station["nodes"]}
    if start_id not in nodes or end_id not in nodes:
        return None
    if start_id == end_id:
        return {"nodes": [nodes[start_id]], "edges": [], "total_minutes": 0}

    adjacency = {node_id: [] for node_id in nodes}
    for edge in station["edges"]:
        adjacency[edge["from"]].append((edge["to"], edge))
        adjacency[edge["to"]].append((edge["from"], edge))

    distances = {node_id: float("inf") for node_id in nodes}
    previous = {}
    distances[start_id] = 0
    queue = [(0, start_id)]

    while queue:
        current_cost, current = heapq.heappop(queue)
        if current_cost != distances[current]:
            continue
        if current == end_id:
            break
        for neighbour, edge in adjacency[current]:
            cost = edge_cost(edge, preference)
            if cost is None:
                continue
            new_cost = current_cost + cost
            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                previous[neighbour] = (current, edge)
                heapq.heappush(queue, (new_cost, neighbour))

    if distances[end_id] == float("inf"):
        return None

    route_nodes = [end_id]
    route_edges = []
    cursor = end_id
    while cursor != start_id:
        parent, edge = previous[cursor]
        route_edges.append(edge)
        route_nodes.append(parent)
        cursor = parent

    route_nodes.reverse()
    route_edges.reverse()
    actual_minutes = sum(edge["minutes"] for edge in route_edges)
    return {
        "nodes": [nodes[node_id] for node_id in route_nodes],
        "edges": route_edges,
        "total_minutes": actual_minutes,
        "preference_score": round(distances[end_id], 1)
    }

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/station")
def get_station():
    return jsonify(load_station())

@app.post("/api/route")
def get_route():
    payload = request.get_json(silent=True) or {}
    start_id = payload.get("start")
    end_id = payload.get("end")
    preference = payload.get("preference", "hurry")
    allowed = {"wheelchair", "hurry", "stairs", "luggage"}
    if preference not in allowed:
        return jsonify({"error": "Unknown travel preference."}), 400
    if not start_id or not end_id:
        return jsonify({"error": "Please select both a starting point and destination."}), 400

    station = load_station()
    route = find_route(station, start_id, end_id, preference)
    if route is None:
        return jsonify({
            "error": "No suitable route was found for this preference. Try another preference or ask station staff for assistance."
        }), 404

    route["preference"] = preference
    route["station_name"] = station["name"]
    return jsonify(route)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "MetroMate API"})

if __name__ == "__main__":
    app.run(debug=True)
