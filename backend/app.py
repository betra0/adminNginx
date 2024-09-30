from flask import Flask, jsonify
import re
import logging

app = Flask(__name__)
log_file_path = '/app/logs/custom_access.log'
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.warning('INIT API.')



def parse_nginx_logs(log_file):
    # Expresión regular para el formato del log
    log_pattern = re.compile(r'\[(?P<time_local>.*?)\] (?P<remote_addr>.*?) "(?P<request_method>.*?) (?P<uri>.*?)" (?P<status>\d+)')
    
    logs = []


    with open(log_file, 'r') as file:
        for line in file:

            match = log_pattern.search(line)
            if match:
                log_entry = {
                    'time_local': match.group('time_local'),
                    'remote_addr': match.group('remote_addr'),
                    'request_method': match.group('request_method'),
                    'uri': match.group('uri'),
                    'status': match.group('status')
                }
                logs.append(log_entry)

    
    return logs

@app.route('/', methods=['GET'])
def liveTest():
    return jsonify({"message": "Hello from the API!"})

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({"message": "Hello!"})

@app.route('/logs', methods=['GET'])
def rutaLogs():


    
    try:
        logs = parse_nginx_logs(log_file_path)
        return jsonify({"message": "", 'data':logs}), 200

    except Exception as e:
        logging.error('Este es un mensaje de error.', e)
        return jsonify({"message": "ERROOOOOOOOR", }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)