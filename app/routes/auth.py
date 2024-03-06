from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..engine import myEngine
from ..OAuth import create_access_token, get_current_user
from ..models import Usuario

router = APIRouter(tags=['Autentication'])
eng = myEngine()

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm=Depends()):
    
    data = eng.login(user_credentials.username, user_credentials.password)
    if not data['validation']:   
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Usuario no encontrado')        
    
    token  = create_access_token({'user':data['rut']})

    eng.registrar_token(user_credentials.username, token=token)

    return {"token": token, "token_type":"bearer"}


@router.post("/Validar_Perfil")
def validar_perfil(req: Usuario, token_data:str = Depends(get_current_user)):
    t=token_data
    d = eng.validar_perfil(req)
    if not d['validation']:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Usuario no encontrado')

    elif not eng.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Inicio sesión en otro equipo')       
    return d
    
    
