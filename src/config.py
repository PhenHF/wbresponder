import os


from dotenv import load_dotenv


load_dotenv()

class Config:
    pass


def get_token():
    config = Config()
    config.token = os.getenv('api_token_1')
    return config.token
