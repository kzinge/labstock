#CASO ESTEJA USANDO DOCKER DESCONSIDERE ESSAS 3 LINHAS:
#from dotenv import load_dotenv
#from os import getenv
#load_dotenv()

def read_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
#Se for usar o docker deve descomentar essas 2 linhas 
SUAP_KEY = read_secret('suap_key')
SUAP_SECRET = read_secret('suap_secret')

#Sem docker:
#SUAP_KEY = getenv('SUAP_KEY')
#SUAP_SECRET = getenv('SUAP_SECRET')

class SuapOAuth2():
    name = 'suap'
    AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
    REVOKE_TOKEN_URL = 'https://suap.ifrn.edu.br/o/revoke_token/'
    ID_KEY = 'identificacao'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'
    SOCIAL_AUTH_SUAP_KEY =  SUAP_KEY
    SOCIAL_AUTH_SUAP_SECRET = SUAP_SECRET

    

    def user_data(self, access_token, *args, **kwargs):
        return self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='GET',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        ).json()

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        você pode fazer aqui outras coisas, como salvar os dados do usuário
        (`response`) em algum outro model.
        """
        splitted_name = response['nome'].split()
        first_name, last_name = splitted_name[0], ''
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        return {
            'username': response[self.ID_KEY],
            'first_name': first_name.strip(),
            'last_name': last_name.strip(),
            'email': response['email'],
        }
