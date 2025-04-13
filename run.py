from src.app import app
from src.app.config import find_free_port

if __name__ == '__main__':
    port = find_free_port(3000)
    print(f'Iniciando aplicação na porta:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)
