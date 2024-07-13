from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Base URL para las APIs
API_BASE_URL = "https://scompcenter.com/david/rest_api_alu_materias_daw/api"

# Ruta para listar todos los registros
@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    response = requests.get(f"{API_BASE_URL}/lista_planes_materias.php")
    data = response.json()

    if search_query:
        filtered_data = [item for item in data['body'] if search_query in str(item.get('cve_plan', '')).lower() or
                         search_query in str(item.get('grado', '')).lower() or 
                         search_query in str(item.get('clave', '')).lower() or 
                         search_query in str(item.get('materia', '')).lower() or 
                         search_query in str(item.get('horas_prac', '')).lower() or 
                         search_query in str(item.get('horas_teo', '')).lower() or 
                         search_query in str(item.get('creditos', '')).lower()]
    else:
        filtered_data = data['body']

    return render_template('index.html', data={'body': filtered_data})




# Ruta para crear un nuevo registro
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form_data = request.form
        payload = {
            'cve_plan': form_data['cve_plan'],
            'grado': form_data['grado'],
            'clave': form_data['clave'],
            'materia': form_data['materia'],
            'horas_prac': form_data['horas_prac'],
            'horas_teo': form_data['horas_teo'],
            'creditos': form_data['creditos']
        }
        response = requests.post(f"{API_BASE_URL}/create_materia.php", json=payload)
        return redirect(url_for('index'))
    return render_template('create.html')

# Ruta para actualizar un registro existente
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        form_data = request.form
        payload = {
            'cve_plan': form_data['cve_plan'],
            'grado': form_data['grado'],
            'clave': form_data['clave'],
            'materia': form_data['materia'],
            'horas_prac': form_data['horas_prac'],
            'horas_teo': form_data['horas_teo'],
            'creditos': form_data['creditos']
        }
        response = requests.post(f"{API_BASE_URL}/update_materia.php", json=payload)
        return redirect(url_for('index'))
    return render_template('update.html')

# Ruta para eliminar un registro
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        form_data = request.form
        payload = {
            'cve_plan': form_data['cve_plan'],
            'clave': form_data['clave']
        }
        response = requests.post(f"{API_BASE_URL}/delete_materia.php", json=payload)
        return redirect(url_for('index'))
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
