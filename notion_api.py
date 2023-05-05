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


def get_person_info(cpf, database_id, headers):
    """
    Queries notion API to find the item ID tied to the passed cpf
        Returns person's Notion ID and Name as a dictionary
        {"id" : "string", "name" : "string"}
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
    pessoa_data = json.loads(response_pessoa.text)

    id_name = {}
    id_name["id"] = pessoa_data['results'][0]['id']
    id_name["name"] = pessoa_data['results'][0]['properties']["API Client"]["formula"]["string"]

    return id_name

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
                        },
                        {
                            "property": "Negociação",
                            "select": {
                                "is_not_empty": True
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

        if sessoes_data['results'][sessao]['properties']['Negociação']["select"] is not None:
            propriedades["Negociação"] = sessoes_data['results'][sessao]['properties']['Negociação']["select"]["name"]
        else:
            propriedades["Negociação"] = None

        if sessoes_data['results'][sessao]['properties']['Sessão']['select'] is not None:
            propriedades["Sessão"] = sessoes_data['results'][sessao]['properties']['Sessão']["select"]["name"]
        else:
            propriedades["Sessão"] = None

        if len(sessoes_data['results'][sessao]['properties']["Briefing"]["rich_text"]) == 0:
            propriedades["Briefing"] = None
        else:
            propriedades["Briefing"] = sessoes_data['results'][sessao]['properties']["Briefing"]["rich_text"][0]["plain_text"]

        propriedades["Pacote"] = sessoes_data['results'][sessao]['properties']["API Pacote"]["formula"]["string"]

        if sessoes_data['results'][sessao]['properties']["API Data"]["formula"]["string"] == "":
            propriedades["Data"] = None
        else:
            propriedades["Data"] = sessoes_data['results'][sessao]['properties']["API Data"]["formula"]["string"]

        if len(sessoes_data['results'][sessao]['properties']["Endereço"]["rich_text"]) == 0:
            propriedades["Endereço"] = None
        else:
            propriedades["Endereço"] = sessoes_data['results'][sessao]['properties']["Endereço"]["rich_text"][0]["plain_text"]

        propriedades["ValorTotal"] = sessoes_data['results'][sessao]['properties']["Valor do Contrato"]["number"]

        todas_sessoes.append(propriedades)

    return todas_sessoes
