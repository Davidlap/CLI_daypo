# TO-DO
# [X] - Mapping between subjects full name and accronyms
# [X] - Function that replace the subjects by the accronyms
# [] - Argparse for year wanted, and subjects, units wanted and if T/F, multiple choice should be included
# [X] - Create a dictionary with the results 
# [] - Transform dictionary into a daypo xml file
# [] - Document the process
# [] - Remove duplicates
# 
import requests
import json
from bs4 import BeautifulSoup
import argparse
import re
import sys



def _parse_arguments():
    parser = argparse.ArgumentParser(description='Configuracion script')

    parser.add_argument('asignatura',  help='Asignatura a extraer', metavar='Asignatura')
    parser.add_argument('unidades',  help='Unidades a escoger', metavar='Unidades', action='append')
    parser.add_argument('--type', help='Tipo de pregunta [vyf, test, multiple]', action='append')
    args = parser.parse_args()

    return args

def fetch_data():
    try:
        print("---- Extracting the data, please wait... ----")
        data = requests.get("http://redoc.live/18-19/db.js") #Make date a variable - argparse
        # As the result is in a .js file, we need to clean up the variable name and convert it to a dictionary
        data_dictionary = json.loads(data.text[data.text.find("{"):])
        print("---- Data extracted sucessfully ----")

        return data_dictionary
    except Exception as ex:
        print("There was a problem while extracting the data " + str(ex))



def replace_subjects_with_acronyms(data):
    
    try:
        with open("subjects_mapping.json", "r", encoding='utf-8') as fp:
            subjects = json.load(fp)
    except Exception as ex:
        print("Error loading the subjects_mapping.json file " + str(ex))

    try:
        print("---- Replacing subject names with their acronyms, please wait... ----")
        for subject_k, subject_v in subjects.items():
            for data_k, data_v in data.items():
                if subject_k == data_k:
                    data[subject_v] = data[data_k]
                    del data[data_k]
                    break
                    
        return data
    except Exception as ex:
        print("Error while replacing subject names with their acronym " + str(ex))

def extract_tests(data_subject, units):
    result = {}
    for data_k, data_v in data_subject.items():
        if data_k in units:
            result[data_k] = data_v
    
    return result

def get_specific_question_type(data_dict, asignatura, question_type_selected=None):
    result = {asignatura: {}}
    for unidad in data_dict.keys():
        result[asignatura]["Unidad-"+unidad]= {"Preguntas":[]}
        lista_preguntas = []
        for question in data_dict[unidad]:
            try:
                soup = BeautifulSoup(question['html'], 'html.parser')
                state_question = soup.find(class_='state').text.lower()
                # print(question)
                number_of_answers = len(soup.find_all(class_=re.compile("r[0-9]+")))
                question_type = soup.find_all(class_=re.compile("r[0-9]+"))[0].input['type']
                question_text = soup.find(class_='qtext').text
                question_answers = soup.find_all(class_=re.compile("r[0-9]+"))

                

                if question_type_selected is not None:
                    if question_type_selected == 'test':
                        if (number_of_answers > 2 and state_question == 'correcta' and question_type == 'radio'):
                            pregunta = {}
                            pregunta['tipo']='Unica solucion'
                            pregunta['pregunta'] = question_text
                            respuestas = {}
                            incorrenct_counter = 0
                            for answer in question_answers:
                                if 'correct' in answer['class']:
                                    respuestas['correcta'] = answer.text.replace('\n','')
                                else:
                                    respuestas['incorrecta-' + str(incorrenct_counter)] = answer.text.replace('\n','')
                                    incorrenct_counter+=1
                            pregunta['respuestas']=respuestas
                            lista_preguntas.append(pregunta)

   
                else:
                    print(f"Question is not only choice it has this amount of answers {number_of_answers}")

            except Exception as ex:
                print("ERROR -- " + str(ex))

        result[asignatura]['Unidad-'+unidad]['Preguntas'].append(lista_preguntas)

    return result


def main():
    args = vars(_parse_arguments())
    asignatura = args['asignatura'].upper()
    unidades = args['unidades'][0].split(',')
    data = fetch_data()
    data_with_acronyms = replace_subjects_with_acronyms(data) #Replace the name of the subject by their acronyms (ie: Acceso a Datos -> AD)
    
    try:
        data_to_extract = data_with_acronyms[asignatura]
    except KeyError:
        print('ERROR - la asignatura extraida no existe, estas son las asignaturas que puedes elegir')
        print([k for k in data_with_acronyms.keys() if len(k) <=5])
        sys.exit(0)

    # Here we call a fnction and pass an argument only one subject from the dictionar, and the list of units
    data_dict = extract_tests(data_to_extract, unidades) 
    data_filtered_by_question_type = get_specific_question_type(data_dict, asignatura, 'test')

    with open('results.json', 'w', encoding='utf-8') as fp:
        json.dump(data_filtered_by_question_type, fp)





if __name__ == "__main__":
    main()