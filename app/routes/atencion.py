from fastapi import APIRouter, status, HTTPException, Depends
from ..engine import myEngine
from ..models import ModuloEstacion, Rut
from ..OAuth import get_current_user


router = APIRouter(tags=['Atención'])
engine = myEngine()
msg_inicio_otro_equipo = 'Inicio sesión en otro equipo'

    
@router.post("/atender_siguiente")
def atender_siguiente(peticion: ModuloEstacion, token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)        
    return engine.atender_siguiente(peticion)

@router.post("/en_atencion")
def en_siguiente(peticion: ModuloEstacion, token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    return engine.en_atencion(peticion)
    
@router.post("/saltar_numero")
def saltar_numero(peticion: ModuloEstacion, token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    return engine.saltar_numero(peticion)
    
@router.post("/cancelar")
def cancelar(rut: Rut, token_data:str = Depends(get_current_user)):
    t = token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    
    return engine.cancelar_numero(rut)

@router.post("/salida")
def salida(rut: Rut, token_data:str = Depends(get_current_user)):
    t = token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    
    return engine.salida_numero(rut)


@router.post("/tecnicos_supervisor")
def tecnicos_supervisor(req: Rut, token_data:str = Depends(get_current_user)):
    t =token_data
    if not engine.check_token(t):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=msg_inicio_otro_equipo)
    
    return engine.get_numeros_supervisor(req)
    
