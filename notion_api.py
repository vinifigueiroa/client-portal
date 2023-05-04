import requests, json, datetime

sessoes_database_id = "b893eec1432d48c985aeb93c40c86941"
pessoas_database_id = "f99ac418abf04ac4b20e78bd491a44ff"

api_token = "secret_xDmLtvuPZQcAfHk4QCajMq4BxnkEZJqJkMmCk9OHLix"

sessoes_database_query_url = "https://api.notion.com/v1/databases/" + sessoes_database_id + "/query"
pessoas_database_query_url = "https://api.notion.com/v1/databases/" + pessoas_database_id + "/query"

pessoas_specifications = {
    "filter": {
        "property": "CPF",
        "rich_text": {
            "contains": "10658545442"
        }
    }
}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": "Bearer " + api_token
}

response_pessoa = requests.post(pessoas_database_query_url, json=pessoas_specifications, headers=headers)
pessoa_id = json.loads(response_pessoa.text)['results'][0]['id']


# for n in range(len(json_respose['results'][0]['properties']['Sessões']['relation'])):
#     sessoes_id.append(json_respose['results'][0]['properties']['Sessões']['relation'][n]['id'])

# print(sessoes_id)


sessoes_specifications = {
    "filter" : {
        "or": [
            {
                "and": [
                    {
                        "property": "Cliente",
                        "relation": {
                         "contains": pessoa_id
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
                            "contains": pessoa_id
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

response_sessoes = requests.post(sessoes_database_query_url, json=sessoes_specifications, headers=headers)
sessoes_data = json.loads(response_sessoes.text)
print("Resultados:", len(sessoes_data['results']))

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

print(todas_sessoes)





# Código da Sessão > title > plain text
#   Negociação > select > name
#   OU Sessão > select > name
# Briefing > rich text > plain text
# Pacote API PACOTE > FORMULA > STRING
# Data de Realização API DATA > FORMULA > STRING
# Endereço > rich text > pain text

# Valor do Contrato > number
# Valor Pago >
# Valor Pendente
