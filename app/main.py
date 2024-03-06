from fastapi import FastAPI, status, HTTPException, Depends
from .engine import myEngine
from .models import Peticion, ModuloEstacion, Rut, Usuario
from .OAuth import get_current_user
from .routes import auth, reversa, atencion
from .config import settings

import pyodbc

engine = myEngine()
app = FastAPI()

app.include_router(auth.router)
app.include_router(reversa.router)
app.include_router(atencion.router)

msg_inicio_otro_equipo = 'Inicio sesión en otro equipo'

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/get_fila")
def get_numeros(token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    
    return engine.get_numeros()
    
@app.get("/get_fila_tv")
def get_fila_tv(token_data: str = Depends(get_current_user)):
    t=token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    return engine.get_fila_tv()

    

    
    
@app.post("/validarcredenciales")
def validar_credenciales(req: Usuario, token_data:str = Depends(get_current_user)):
    t = token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    
    res = engine.validar(req)
    return {'validation': res}

        
@app.post("/get_fila_num")
def get_numeroApp(req: Rut, token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    return engine.get_numeroApp(req)
    
            