from flask import Flask, request, render_template, redirect, send_file, jsonify
from base_func import (newton_raphson,iterate_values,file_path,periodic_cleaner)
from datetime import datetime
import json
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/math/<url>', methods=['GET', 'POST'])
def base_urls(url):
    data = request.base_url
    results = []
    if request.method == 'POST': 
        try:
            func1 = request.form.get('func1')  
            func2 = request.form.get('func2')  
            start_x = float(request.form.get('start_x'))
            start_y = float(request.form.get('start_y'))
            epsilon = float(request.form.get('Epslon'))
            if str(url) ==str('itaratsiya'):
                results = iterate_values(func1, func2, start_x, start_y, epsilon)
                filename = f'itaratsiya_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                json_path = file_path(filename)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({'iterations': results}, f, indent=4)
                return render_template(
                'itaratsiya.html',results=results,data=data,error=None,filename=filename)
            elif str(url)==str('nyuton_itaratsiya'):
                results = newton_raphson(func1, func2, start_x, start_y, epsilon)
                filename = f'nyuton_itaratsiya_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                json_path = file_path(filename)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({'iterations': results}, f, indent=4)
                return render_template('nuyuton_itaratsiya.html',results=results,data=data,error=None,filename=filename)
            else:
                return redirect('/')
  
        except Exception as e:
            return render_template('input.html', error=str(e),data=data, results=[])

    return render_template('input.html', results=[],data=data,error=None)


@app.route('/developer')
def developer():
    return render_template('developer.html')

# JSON yuklab olish
@app.route('/download/<file_name>')
def download_file(file_name):
    try:
        json_path = file_path(f'{file_name}.json')
        download_filename = file_name.rsplit('_', 2)[0]
        return send_file(json_path, as_attachment=True, download_name=download_filename, mimetype='application/json')
    except Exception:
        return redirect('/')

# API orqali natijalarni olish
@app.route('/api/math/<url>', methods=['POST'])
def api_math(url):
    try:
        data = request.get_json()

        func1 = data.get('func1')
        func2 = data.get('func2')
        start_x = float(data.get('start_x'))
        start_y = float(data.get('start_y'))
        epsilon = float(data.get('epsilon'))

        results = []

        if url == str('itaratsiya'):
            results = iterate_values(func1, func2, start_x, start_y, epsilon)
            filename = f'itaratsiya_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        elif url == str('nyuton_itaratsiya'):
            results = newton_raphson(func1, func2, start_x, start_y, epsilon)
            filename = f'nyuton_itaratsiya_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        else:
            return jsonify({"error": "Unknown method"}), 400

        json_path = file_path(filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({'iterations': results}, f, indent=4)

        return jsonify({"result": results, "file_saved": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    threading.Thread(target=periodic_cleaner, daemon=True).start()
    app.run(debug=True)
