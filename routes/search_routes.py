from flask import Blueprint, render_template, request
from db.connection import db_query_all

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    min_lat = request.args.get("min_lat", "").strip()
    max_lat = request.args.get("max_lat", "").strip()
    min_lon = request.args.get("min_lon", "").strip()
    max_lon = request.args.get("max_lon", "").strip()
    
    sql = "SELECT s.*, u.username as owner_name FROM parking_spot s JOIN users u ON s.owner_id = u.id WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (s.title LIKE ? OR s.description LIKE ? OR s.address LIKE ? OR s.tags LIKE ?)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q, like_q, like_q])
        
    if min_lat and max_lat and min_lon and max_lon:
        try:
            min_lat_f = float(min_lat)
            max_lat_f = float(max_lat)
            min_lon_f = float(min_lon)
            max_lon_f = float(max_lon)
            sql += " AND s.lat BETWEEN ? AND ? AND s.lon BETWEEN ? AND ?"
            params.extend([min_lat_f, max_lat_f, min_lon_f, max_lon_f])
        except ValueError:
            pass
            
    sql += " ORDER BY s.created_at DESC"
    spots = db_query_all(sql, params)
    
    return render_template("search.html", spots=spots, query=query, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
