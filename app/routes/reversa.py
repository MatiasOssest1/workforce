from fastapi import APIRouter, Depends, status, HTTPException
from ..engine import myEngine
from ..OAuth import get_current_user
from ..models import listaTIF

router = APIRouter(tags=['Reversa'])
eng = myEngine()

@router.get("/reversa/{rut}")
def get_reversa(rut, token_data: str= Depends(get_current_user)):
    t = token_data
    try:
        res = eng.get_reversa(rut=rut)
        return {"data": res}
    
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/reversa_pendiente/{rut}")
def get_reversa_pendiente(rut:str, token_data: str= Depends(get_current_user)):
    t = token_data
    try: 
        res = eng.get_reversa_pendiente(rut=rut)

        return {"data": res}
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/reversa_pendiente")
def actualizar_impresion(req: listaTIF , token_data: str= Depends(get_current_user)):
    t = token_data

    try:
        eng.update_TIF(tifs=req)
        return {"detail": "Actualizado correctamente"}
    
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


    
    