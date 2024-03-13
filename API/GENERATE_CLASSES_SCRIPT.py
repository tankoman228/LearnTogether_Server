import os


# Функция для поиска строк с нужными аннотациями в файле
def find_annotations(file_path):
    annotations = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace("@api.", "@app.")
            if "@app.put" in line or "@app.delete" in line or "@app.post" in line:
                annotations.append(line.strip())
    return annotations


# Функция для создания интерфейса на Java
def generate_java_interface(annotations):
    java_interface = "import retrofit2.Call;\nimport retrofit2.http.Body;\nimport retrofit2.http.POST;\nimport retrofit2.http.DELETE;\nimport retrofit2.http.PUT;\n\npublic interface ApiServiceInterface {\n\n"

    for annotation in annotations:
        method_type = "POST" if "@app.post" in annotation else "PUT" if "@app.put" in annotation else "DELETE"
        endpoint = annotation.replace('@app.post','').replace('@app.put','').replace('@app.delete','').replace('(','').replace(')','').replace('\"','').replace('\'','')
        java_interface += f"\t@{method_type}(\"{endpoint}\")\n"
        java_interface += f"\tCall<ResponseU> {endpoint.replace('/', '_')}(@Body RequestU request);\n\n"

    java_interface += "}"
    return java_interface


# Путь к директории с файлами Python
directory_path = ""

# Получаем список файлов .py в директории
python_files = [file for file in os.listdir() if file.endswith(".py")]

annotations = []
for file_name in python_files:
    file_path = file_name
    annotations.extend(find_annotations(file_path))

java_interface = generate_java_interface(annotations)

print(java_interface)