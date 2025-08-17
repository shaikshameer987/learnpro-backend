import environ

env = environ.Env()
environ.Env.read_env()

def is_production():
     return env('ENVIRONMENT') == "PRODUCTION"