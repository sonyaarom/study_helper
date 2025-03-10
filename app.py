from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
from config import config

app = Flask(__name__)

def get_db_connection():
    """Create a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=config.db_name,
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port
    )
    conn.cursor_factory = psycopg2.extras.DictCursor
    return conn

@app.route('/')
def index():
    """Render the main page with all universities."""
    return render_template('index.html')

@app.route('/api/universities')
def get_universities():
    """API endpoint to get universities with optional filters."""
    # Get filter parameters
    hochschule_or_uni = request.args.get('type')
    entrance_test_online = request.args.get('online')
    public = request.args.get('public')
    
    # Build the query
    query = "SELECT * FROM universities WHERE 1=1"
    params = []
    
    if hochschule_or_uni:
        query += " AND hochschule_or_uni = %s"
        params.append(hochschule_or_uni)
    
    if entrance_test_online is not None:
        online_bool = entrance_test_online.lower() == 'true'
        query += " AND entrance_test_online = %s"
        params.append(online_bool)
    
    if public is not None:
        public_bool = public.lower() == 'true'
        query += " AND public = %s"
        params.append(public_bool)
    
    # Order by name
    query += " ORDER BY stk_name"
    
    # Execute the query
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            universities = [dict(row) for row in cur.fetchall()]
        return jsonify(universities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/university/<university_id>')
def get_university(university_id):
    """API endpoint to get details for a specific university."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM universities WHERE university_id = %s", (university_id,))
            university = dict(cur.fetchone()) if cur.rowcount > 0 else None
        
        if university:
            return jsonify(university)
        else:
            return jsonify({"error": "University not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/favorites')
def favorites():
    """Render the favorites page."""
    return render_template('favorites.html')

if __name__ == '__main__':
    app.run(debug=True) 