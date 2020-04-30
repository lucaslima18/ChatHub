import sys, os
import json, requests, time
from settings import REPOSITORY_UUID, LANGUAGE, AUTH_TOKEN, SERVICE_TYPE

repository = REPOSITORY_UUID
headers = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}

#Chatito functions
def readIntents():
    chatito_files = os.listdir("project/chatito_files/")
    for file_name in chatito_files:
        # inserir verificações depois
        intent = file_name.split('.')[0]
        chatito_file = file_name
        print(intent, chatito_file)
        generateRasaPhrases(chatito_file, intent)
        
def generateRasaPhrases(chatito_file, intent):
    # inserir verificações depois
    print(chatito_file)
    os.system(
        f'npx chatito project/chatito_files/{chatito_file} --format "rasa" --outputPath "project/json_files" --trainingFileName "{intent}_training.json" --testingFileName "{intent}_testing.json"'
    )

#Bothub functions
def get_examples_count(*args):
    return json.loads(requests.get(
        f'https://api.bothub.it/v2/repository/repository-info/{REPOSITORY_UUID}',
        headers=headers
    ).content).get('examples__count')

def delete_repository():
    return requests.delete(
        f'https://api.bothub.it/v2/repository/repository-info/{REPOSITORY_UUID}/',
        headers=headers
    )

def get_all_examples(headers, next_call, repository, *args):
    while next_call is not None:
        response = requests.get(next_call, headers=headers, params={"repository_uuid": repository})
        response_json = response.json()
        next_call = response_json.get('next')
        yield response_json.get('results', None)

def delete_example(example_id, *args):
    response = requests.delete(f'https://api.bothub.it/v2/repository/example/{example_id}/', headers=headers)
    if response.status_code == 204:
        print("Example deleted!")
        print(response.status_code)
        return response.status_code

def create_example(example, repository, *args):
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
        if response.status_code == 400:
            return 'Existing Example!'
        
        elif response.status_code == 201:
            return 'Example created!'

        return response.status_code
    
    except err: 
        print(err) 
        print(f'Failed to train this sentence!\nText: {example.get("text")}')
        return

def create_evaluate_examples(example, repository, *args):
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
        "language": LANGUAGE,
        "intent": example.get('intent'),
        "entities": entities
    }
    try: 
        response = requests.post('https://api.bothub.it/v2/repository/evaluate/', headers=headers, data=json.dumps(data))
        if response.status_code == 400:
            return 'Existing Example!'
        
        elif response.status_code == 201:
            return 'Example created!'

        return response.status_code
    
    except err: 
        print(err) 
        print(f'Failed to train this sentence!\nText: {example.get("text")}')
        return


def delete_all(repository):
    count = get_examples_count(repository)
    results = get_all_examples(
        headers=headers,
        next_call='https://api.bothub.it/v2/repository/examples/',
        params={"repository_uuid": repository}
    )
    index = 0

    for result in results:
        for item in result:
            time.sleep(1)
            delete_example(item.get('id'))
            index += 1
            print(f"%.2f%%" % ((index*100)/count))

def mountDict(file_name, repository, service):
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
                if service == 'training' or service == '1':
                    print(f"%.2f%%" % ((index*100)/count), create_example(result, repository), end='\r')
                    
                
                elif service == 'testing' or service == '2':
                    print(f"%.2f%%" % ((index*100)/count), create_evaluate_examples(result, repository), end='\r')

#main functions
def runTraining():
    diretorios = os.listdir('project/json_files')
    print(diretorios)

    for file_name in diretorios:
        file_extention = file_name.split('_')[1]
        print(file_extention)
        
        if file_extention == 'training.json':
            service = 'training'
            mountDict(file_name, repository, service)

        if file_extention == 'testing.json':
            pass

def runTesting():
    diretorios = os.listdir('project/json_files')

    for file_name in diretorios:
        file_extention = file_name.split('_')[1]
        
        if file_extention == 'training.json':
            pass

        if file_extention == 'testing.json':
            service = 'testing'
            result = mountDict(file_name, repository, service)

def get_repository_uuid(service):
    files = os.listdir("project/json_files/")
    binary_answers = input("you go training all files on same repository? [y/n] ")
    
    if binary_answers == 'y':
        repository = input('enter the uuid intelligence repository: ')
        runTraining()

    else:
        print("OUTRO")
        for file_name in files:
            print(service, file_name, file_name.split('_'))
            if service == "training" or service == "1":
                if file_name.split('_')[1] == 'training.json':
                    repository = input(f"type the repository_uuid of the intelligence belonging to the file {file_name}: ")
                    mountDict(file_name, repository, service)

                else:
                    pass
            
            elif service == "testing" or service == "2":
                if file_name.split('_')[1] == 'testing.json':
                    repository = input(f"type the repository_uuid of the intelligence belonging to the file {file_name}: ")
                    mountDict(file_name, repository, service)

                else:
                    pass
            
