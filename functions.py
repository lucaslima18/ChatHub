import sys, os
import json, requests, time
from settings import REPOSITORY_UUID, LANGUAGE, AUTH_TOKEN

'''
repository = 'c4bf350f-e678-490e-b5ca-c0a2b1b52b93'
params= {"repository_uuid": repository}
headers = {
    "Authorization": "Token 5ef90351e1b8bb19761e98e03773f0d20f3f94de",
    "Content-Type": "application/json"
}
'''
repository = REPOSITORY_UUID
params= {"repository_uuid": repository}
headers = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}

#Chatito functions
def readIntents():
    with open("project/intents.txt") as intents_list:

        for line in intents_list:
            # inserir verificações depois
            intent = line.strip()
            chatito_file = f"{intent}.chatito"
            generateRasaPhrases(chatito_file, intent)
            print(intent)

def generateRasaPhrases(chatito_file, intent):
    # inserir verificações depois
    print(chatito_file)
    os.system(
        f'npx chatito project/intents/{chatito_file} --format "rasa" --outputPath "project/json_files" --trainingFileName "{intent}_training.json" --testingFileName "{intent}_testing.json"'
    )

#Bothub functions
def get_examples_count(*args):
    return json.loads(requests.get(
        f'https://api.bothub.it/v2/repository/repository-info/{repository}',
        headers=headers
    ).content).get('examples__count')

def delete_repository():
    return requests.delete(
        f'https://api.bothub.it/v2/repository/repository-info/{repository}/',
        headers=headers
    )

def get_all_examples(headers, next_call, params, *args):
    while next_call is not None:
        response = requests.get(next_call, headers=headers, params=params)
        response_json = response.json()
        next_call = response_json.get('next')
        yield response_json.get('results', None)

def delete_example(example_id, *args):
    response = requests.delete(f'https://api.bothub.it/v2/repository/example/{example_id}/', headers=headers)
    if response.status_code == 204:
        print("Example deleted!")
        print(response.status_code)
        return response.status_code

def create_example(example, *args):
    entities = []
    if len(example.get('entities')) > 0:
        for entity in example.get('entities'):
            if entity:
                entities.append({
                    "entity": entity.get('entity'),
                    "start": entity.get('start'),
                    "end": entity.get('end')
                })

    data = {
        "repository": repository,
        "text": example.get('text'),
        "intent": example.get('intent'),
        "entities": entities
    }
    try: 
        response = requests.post('https://api.bothub.it/v2/repository/example/', headers=headers, data=json.dumps(data))
        print("Example created!")
        return response.status_code
    except err: 
        print(err) 
        print(f'Failed to train this sentence!\nText: {example.get("text")}')
        return

def create_evaluate_examples(file_name, *args):
    with open(f'project/json_files/{file_name}') as json_file:
        examples = json.load(json_file)
        index = 0
        for intent, texts in examples.items():
            for text in texts:
                data = {
                    "repository": repository,
                    "language": "pt_br",
                    "entities": [],
                    "text": text,
                    "intent": intent
                }
                response = requests.post('https://api.bothub.it/v2/repository/evaluate/', headers=headers, data=json.dumps(data))
                print(response.status_code)
                if response.status_code == 201:
                    print("\nEvaluate example created!")

def delete_all():
    count = get_examples_count(repository)
    results = get_all_examples(
        headers=headers,
        next_call='https://api.bothub.it/v2/repository/examples/',
        params=params
    )
    index = 0

    for result in results:
        for item in result:
            time.sleep(1)
            delete_example(item.get('id'))
            index += 1
            print(f"%.2f%%" % ((index*100)/count))

def mountDict(file_name, service):
        with open(f'project/json_files/{file_name}') as json_file:
            examples = json.load(json_file)['rasa_nlu_data']['common_examples']
            count = len(examples)
            index = 0
            
            for example in examples:
                entities = []
        
                for entity in example['entities']:

                    entities.append({
                        "entity": entity['entity'],
                        "start": entity['start'],
                        "end": entity['end']
                    })

                result = {
                    "text": example['text'],
                    "language": LANGUAGE,
                    "intent": example['intent'], 
                    "entities": entities
                }
                texto = example['text']
                entidades = entities
                intencao = example['intent']
                linguagem = 'pt_br'
                index += 1
                print(f"%.2f%%" % ((index*100)/count))

                if service == 'training':
                    create_example(result)
                
                elif service == 'testing':
                    print("OLHA O TREINO")
                    create_evaluate_examples(file_name,result)

                else:
                    print("NAO ROLOU")
#main functions
def runTraining():
    diretorios = os.listdir('project/json_files')
    print(diretorios)

    for file_name in diretorios:
        file_extention = file_name.split('_')
        file_extention = file_extention[1]
        print(file_extention)
        
        if file_extention == 'training.json':
            service = 'training'
            mountDict(file_name, service)

        if file_extention == 'testing.json':
            pass

def runTesting():
    diretorios = os.listdir('project/json_files')
    print(diretorios)
    
    for file_name in diretorios:
        print(file_name)
        file_extention = file_name.split('_')
        file_extention = file_extention[1]
        
        if file_extention == 'training.json':
            pass

        if file_extention == 'testing.json':
            service = 'testing'
            mountDict(file_name, service)
