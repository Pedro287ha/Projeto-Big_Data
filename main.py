from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import pandas as pd



# estrutando o programa em classe seguindo a documentacao do fast api e do w3school
# https://www.w3schools.com/python/python_classes.asp


# classe para gerenciar movimentacao do arquivo
class FileManager: 
    def __init__(self, upload_dir="./uploaded_files"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: UploadFile):
        file_path = os.path.join(self.upload_dir, "dados.ods")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def extract_data(self, file_path):
        conteudo = {
            "Pratos": [],
            "Valores": [],
            "Data_compras": [],
            "Meio_pagamentos": []
        }
        df = pd.read_excel(file_path, engine='odf')

        if not df.empty:  # arquivo possui conteudo ? 

            #
            dados_arquivo = df[['Prato', 'Valor', 'Data da Compra', 'Meio de Pagamento']]
            
            dados = dados_arquivo.to_dict(orient='records')
            for item in dados:
                conteudo["Pratos"].append(item['Prato'])
                conteudo["Valores"].append(item['Valor'])
                conteudo["Data_compras"].append(item['Data da Compra'])
                conteudo["Meio_pagamentos"].append(item['Meio de Pagamento'])

            return conteudo

        return []

# classe principal 
class MyApp:
    def __init__(self):
        self.app = FastAPI()
        self.file_manager = FileManager()
        
        # Corrigindo problema do carregamento de imagens 
        self.app.mount("/static", StaticFiles(directory="static"), name="static") #https://stackoverflow.com/questions/70632673/fastapi-is-not-loading-static-files
        
        self.setup_routes()
        self.setup_middleware()

    # Resolvendo problema de redirecionamento 
    def setup_middleware(self): # parte do codigo retirado de https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi
        self.app.add_middleware( # https://stackoverflow.com/questions/73607320/fastapis-redirectresponse-doesnt-work-as-expected-in-swagger-ui
            CORSMiddleware, # https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


    # criando rotas da api
    def setup_routes(self): # exemplos retirados de https://stackoverflow.com/questions/63853813/how-to-create-routes-with-fastapi-within-a-class
        @self.app.get("/", response_class=HTMLResponse)
        async def read_root():
            with open("static/index.html") as f:
                return f.read()

        @self.app.post("/uploadfile/")
        async def upload_file(file: UploadFile = File(...)):
            file_path = self.file_manager.save_file(file)
            # enviando codigo de redirecionamento para como resposta junta a pagina
            
            # o script de fetch na paginaestara aguardando um redirect
            return RedirectResponse(url='/grafico', status_code=303)

        @self.app.get("/grafico", response_class=HTMLResponse) 
        async def show_graph_page():
            # parte onde informacoes dos dados serao mostrados
            with open("static/graficos.html") as f:
                return f.read()

        @self.app.get("/data") # rota para receber dados do arquivo
        async def fetch_data():
            dados = self.file_manager.extract_data(os.path.join(self.file_manager.upload_dir, "dados.ods"))
            return dados

if __name__ == "__main__" or True:
    app_instance = MyApp()
    app = app_instance.app
