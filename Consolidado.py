from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time

# Conexão com o Mongo Atlas
# Importação dos pacotes necessários
MONGODB_URI = "XXXXXXXXX"

client = MongoClient (MONGODB_URI)

# Checagem para ver se a conexão está funcionamento corretamente
# Check to see if the connection is working correctly
for db_name in client.list_database_names():
    print(db_name)


# Inicialização do client Mongo e criação do BD
# Initializing the Mongo client and creating the database
db = client['kabum']

# Inserção do nome dos departamentos em uma lista
# Insertion of department names into a list
departamentos = ["Perifericos", "Computadores", "Placa-de-Video-vga", "Monitores", "Gamer", "Audio", "TV", "eletrodomesticos", "eletroportateis", "casa-inteligente", "Ferramentas", "ar-e-ventilacao", "Seguranca", "Notebook", "cameras-e-drones", "Conectividade", "Processadores", "Geek", "Espaco-Gamer", "Escritorio", "Energia", "servicos-digitais"]

# Criação de um loop com a lista de departamentos para fazer a extração dos produtos de cada um em uma collection distinta
# Creating a loop with the list of departments to extract products from each one into a separate collection
for departamento in departamentos:  
    print(f"Coletando dados para o departamento: {departamento}")

# Criação da collection no Mongo
# Creation of the collection in Mongo
    collection = db[departamento]

# Inicialização do driver utilizado pelo Selenium
# Initialization of the driver used by Selenium
    driver = webdriver.Chrome()

# Inserção do "departamento" inserido no site da Kabum para iniciar a raspagem
# Insertion of the "department" entered on the Kabum website to start scraping
    url = f"https://www.kabum.com.br/{departamento.lower()}"
    driver.get(url)

    while True:
# Inseri uma pequena pausa para garantir que a URL esteja completamente carregada
# Inserted a short pause to ensure the URL is fully loaded
        time.sleep(5)

# Busca dos elementos que contém o nome e o preço dos produtos. Você pode inserir mais elementos caso deseje
# Searching for elements that contain the name and price of products. You can insert more elements if desired
        produtos = driver.find_elements(By.CSS_SELECTOR, ".sc-d79c9c3f-0")
        precos = driver.find_elements(By.CSS_SELECTOR, ".sc-3b515ca1-2") 

# Inserção dos dados na collection do Mongo
# Insertion of data into the Mongo collection
        for produto, preco in zip(produtos, precos):
            data = {
                'produto': produto.text.strip(),
                'preco': preco.text.strip()
            }
            collection.insert_one(data)

# Busca pelo botão "próxima página" para percorrer todo o departamento
# Searching for the "next page" button to browse through the entire department
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.nextLink')))
            next_button.click()
        except:
            print("Nenhuma outra página encontrada. Saindo.")
            break

# Fechamento do driver
# Closing the driver
    driver.quit()

# Confirmação do procedimento
# Confirmation of the procedure
print("Dados inseridos com sucesso.")