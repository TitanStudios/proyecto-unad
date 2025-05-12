from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unad2025'

# Configuración de la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tablas (ejecutar solo una vez)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            data_type TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            date_detected TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Datos de ejemplo (simulación OSINT)
sample_alerts = [
    {"source": "Dark Web Forum", "data_type": "Correo institucional", "risk_level": "Alto", "date_detected": "2025-05-10"},
    {"source": "HaveIBeenPwned", "data_type": "Contraseña", "risk_level": "Medio", "date_detected": "2025-05-09"},
]

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Panel de control
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    alerts = conn.execute('SELECT * FROM alerts ORDER BY date_detected DESC').fetchall()
    conn.close()
    return render_template('dashboard.html', alerts=alerts)

# Simular detección de filtraciones
@app.route('/scan', methods=['POST'])
def scan():
    conn = get_db_connection()
    for alert in sample_alerts:
        conn.execute('INSERT INTO alerts (source, data_type, risk_level, date_detected) VALUES (?, ?, ?, ?)',
                     (alert['source'], alert['data_type'], alert['risk_level'], alert['date_detected']))
    conn.commit()
    conn.close()
    flash('¡Escaneo completado! Se detectaron nuevas filtraciones.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True)

@app.route('/clear_alerts', methods=['POST'])
def clear_alerts():
    conn = get_db_connection()
    conn.execute('DELETE FROM alerts')
    conn.commit()
    conn.close()
    flash('Todas las alertas han sido eliminadas correctamente', 'success')
    return redirect(url_for('dashboard'))