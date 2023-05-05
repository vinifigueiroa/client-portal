import requests, json, datetime

def make_headers(api_token):
    """ It takes an api_token as input and returns a
    dictionary of headers to be used in an HTTP
    request to the Notion API.
    """
    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer " + api_token
    }


def get_person_id(cpf, database_id, headers):
    """
    Queries notion API to find the item ID tied to the passed cpf
        Returns person's Notion ID as a string
    """

    pessoas_specifications = {
        "filter": {
            "property": "CPF",
            "rich_text": {
                "contains": cpf
            }
        }
    }

    pessoas_database_query_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
    response_pessoa = requests.post(pessoas_database_query_url, json=pessoas_specifications, headers=headers)
    return json.loads(response_pessoa.text)['results'][0]['id']

def get_sessoes(person_id, database_id, headers):

    sessoes_specifications = {
        "filter" : {
            "or": [
                {
                    "and": [
                        {
                            "property": "Cliente",
                            "relation": {
                            "contains": person_id
                            }
                        },
                        {
                            "property": "Negociação",
                            "select": {
                                "equals": "Contratada"
                            }
                        },
                        {
                            "property": "Sessão",
                            "select": {
                                "is_not_empty": True
                            }
                        },
                    ]
                },
                {
                    "and" : [
                        {
                            "property": "Cliente",
                            "relation": {
                                "contains": person_id
                            }
                        },
                        {
                            "property": "Negociação",
                            "select": {
                                "does_not_equal": "Oportunidade"
                            }
                        },
                        {
                            "property": "Negociação",
                            "select": {
                                "does_not_equal": "Abandonada"
                            }
                        },
                        {
                            "property": "Negociação",
                            "select": {
                                "does_not_equal": "Contratada"
                            }
                        }
                    ]
                }
            ]
        },
        "sorts": [
            {
                "property": "Código da Sessão",
                "direction": "descending"
            }
        ]
    }

    sessoes_database_query_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
    response_sessoes = requests.post(sessoes_database_query_url, json=sessoes_specifications, headers=headers)
    sessoes_data = json.loads(response_sessoes.text)

    todas_sessoes = []

    for sessao in range(len(sessoes_data['results'])):
        propriedades = {}
        propriedades["Código"] = sessoes_data['results'][sessao]['properties']['Código da Sessão']["title"][0]["plain_text"]
        propriedades["Negociação"] = sessoes_data['results'][sessao]['properties']['Negociação']["select"]["name"]

        if sessoes_data['results'][sessao]['properties']['Sessão']['select'] is not None:
            propriedades["Sessão"] = sessoes_data['results'][sessao]['properties']['Sessão']["select"]["name"]
        else:
            propriedades["Sessão"] = None
        todas_sessoes.append(propriedades)

        propriedades["Briefing"] = sessoes_data['results'][sessao]['properties']["Briefing"]["rich_text"][0]["plain_text"]
        propriedades["Pacote"] = sessoes_data['results'][sessao]['properties']["API Pacote"]["formula"]["string"]

        if len(sessoes_data['results'][sessao]['properties']["Endereço"]["rich_text"]) == 0:
            propriedades["Endereço"] = None
        else:
            propriedades["Endereço"] = sessoes_data['results'][sessao]['properties']["Endereço"]["rich_text"][0]["plain_text"]

        propriedades["Valor Total"] = sessoes_data['results'][sessao]['properties']["Valor do Contrato"]["number"]

    return todas_sessoes
