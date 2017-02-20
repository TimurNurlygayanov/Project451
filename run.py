from app import app, cfg

if __name__ == '__main__':
    app.run(debug=cfg.AppConfig['DEBUG_MODE'],
            host=cfg.AppConfig['HOST'],
            port=cfg.AppConfig['PORT'])
