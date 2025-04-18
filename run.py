from src.app import app

if __name__ == '__main__':
    print('Iniciando aplicação na porta: 5000')
    app.run(host='0.0.0.0', port=5000, debug=True)