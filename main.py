from settings import *
from functions import *

if SERVICE_TYPE == 'clear':
    sure = input("Tem certeza que deseja deletar? [y/n]\n")
    
    if sure == 'y':
        print("limpando")
        delete_all()
    
    elif sure == 'n':
        print("parando programa")

elif SERVICE_TYPE == 'testing':
    print("cirar testes")
    readIntents()
    runTesting()
    

elif SERVICE_TYPE == 'training':
    print("criar treinos")
    readIntents()
    runTraining()
    
