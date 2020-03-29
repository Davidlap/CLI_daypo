# TO-DO
# [X] - Mapping between subjects full name and accronyms
# [X] - Function that replace the subjects by the accronyms
# [] - Argparse for year wanted, and subjects, units wanted and if T/F, multiple choice should be included
# [] - Create a dictionary with the results 
        # {"AD":{
        #     "Unidad-1":{
        #         "Preguntas":[
                        # {
                        #     "Tipo": "Unica solucion",
                        #     "Correcta": 2,
                        #     "Detalles":{
                        #         "Pregunta": "blablablabla",
                        #         "Respuestas": ["1-blabla, 2-blabla, 3-blabla, 4-blabla"]

                        #     }
                        # }

        #         ]
        #     }
        # }}
# [] - Transform dictionary into a daypo xml file
# [] - Document the process
# 
import requests
import json
from bs4 import BeautifulSoup
import argparse





# def _parse_arguments():
#     parser = argparse.ArgumentParser(description='Process configuration needed')

#     parser.add_argument('path',  help='Path to the folder', type=str, metavar='path')
#     parser.add_argument('-r',  help='Regular expresion to split the directory name', default=' [', type=str, metavar='')
#     parser.add_argument('-e', help='Movie file extensions', default=['.avi', '.mkv', '.mp4'], action='append', metavar='')
#     args = parser.parse_args()

#     return args

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
        with open("subjects_mapping.json", "r") as fp:
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

def main():
    # args = vars(_parse_arguments())

    # directory_path = args['path']
    data = fetch_data()
    data_with_acronyms = replace_subjects_with_acronyms(data) #Replace the name of the subject by their acronyms (ie: Acceso a Datos -> AD)
    print(data_with_acronyms.keys())







if __name__ == "__main__":
    main()