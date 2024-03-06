from sqlalchemy import create_engine, text
from .models import Peticion, Numero, ModuloEstacion, Rut, Usuario, TokenData, listaTIF
from .config import settings

def get_numero_to_dict(res):
    d = {"rut": res[0], "numero": str(res[1]), "estacion": res[2],
    "estado": res[3], "proceso": res[4]}
    return d

def get_numeros_to_dict(res):
    l = []
    for row in res:
        l.append({"rut": row[0], 'nombre': row[1] ,"numero": row[2], "estacion": row[3],
        "estado": row[4], "proceso": row[5]}) 
    return l

def get_numerostv_to_dict(res):
    l = []
    for row in res:
        l.append({"rut": row[0], 'nombre': row[1] ,"numero": row[2], "estacion": row[3],
        "atendedor":row[4],"estado": row[5], "proceso": row[6]}) 
    return l

def get_numero_app(res):
    d = {"numero": res[0], "estacion": res[1], "estado": res[2]}
    return d


def get_numero_to_app(res) :
    return {"numero": res[0], "estacion": res[1], "estado": res[2]}

def reversa_to_dict(res, pendiente=False):
    l = []
    if pendiente:
        for row in res:
            if row[9]==0:
                l.append({'id':row[0], 'nombre':row[1].title(), 'rut': row[2], 'fecha': row[3].strftime('%d-%m-%Y'), 'orden': row[4], 'ANI': row[5],
                        'clave': row[6], 'causa': row[7], 'equipo': row[8], 'entregado': row[9],
                        'fuente': row[10], 'impresion': row[11]})        
    else:
        for row in res:
            l.append({'id':row[0], 'nombre':row[1].title(), 'rut': row[2], 'fecha': row[3].strftime('%d-%m-%Y'), 'orden': row[4], 'ANI': row[5],
                    'clave': row[6], 'causa': row[7], 'equipo': row[8], 'entregado': row[9],
                    'fuente': row[10], 'impresion': row[11]})
    return l



class myEngine:
    
    def __init__(self) -> None:
        self.__engine = create_engine(f"mssql+pyodbc://{settings.database_user}:{settings.database_password}@{settings.database_url}/{settings.database_schema}?driver=ODBC+Driver+17+for+SQL+Server")

    def dar_numero(self, peticion: Peticion):
        with self.__engine.connect() as conn:
            conn.execute(text(f"EXEC DAR_NUMERO '{peticion.rut}', {peticion.proceso_id}"))
            conn.commit()
            
            res = conn.execute(text(f"EXEC GET_NUMERO '{peticion.rut}'")).fetchone()
            return  get_numero_to_dict(res)
    
    def get_fila_tv(self):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_NUMEROS2")).fetchall()
            res = get_numerostv_to_dict(res)
            return {"data": res}

    def get_numeros(self):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_NUMEROS")).fetchall()
            l = get_numeros_to_dict(res)
            return {"data": l}

    def atender_siguiente(self, peticion: ModuloEstacion):
        with self.__engine.connect() as conn:
            conn.execute(text(f"EXEC ATENDER_SIGUIENTE {peticion.estacion}, {peticion.modulo}"))
            conn.commit()
            
            res = conn.execute(text(f"""select p.nombre, a.Numero, a.Rut from EnAtencion as a
                                       join Persona as p 
                                       on a.Rut=p.numDoc
                                       where estacion_id={peticion.estacion} and  modulo={peticion.modulo}""")).fetchone()
            if res:
                return {'nombre': res[0], 'numero': res[1], 'rut': res[2]}
            
            return {'nombre': 'Nadie en la fila', 'numero': -1, 'rut': None}   

    def saltar_numero (self, peticion : ModuloEstacion):
        with self.__engine.connect() as conn:
            conn.execute(text(f"EXEC SALTAR_NUMERO {peticion.estacion}, {peticion.modulo}"))
            conn.commit() 
       
            res = conn.execute(text(f"""select p.nombre, a.Numero, a.Rut from EnAtencion as a
                                       join Persona as p 
                                       on a.Rut=p.numDoc
                                       where estacion_id={peticion.estacion} and  modulo={peticion.modulo}""")).fetchone()
            if res:
                return {'nombre': res[0], 'numero': res[1], 'rut':res[2]}
            
            return {'nombre': 'Nadie en la fila', 'numero': -1, 'rut': None}
            
    def en_atencion(self, peticion: ModuloEstacion):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"""select p.nombre, a.Numero, a.Rut from EnAtencion as a
                                       join Persona as p 
                                       on a.Rut=p.numDoc
                                       where estacion_id={peticion.estacion} and  modulo={peticion.modulo}""")).fetchone()
            if res:
                return {'nombre': res[0], 'numero': res[1], 'rut':res[2]}
            
            return {'nombre': 'Nadie en atención', 'numero': -1, 'rut': None}
                
    def cancelar_numero(self, peticion : Rut):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_NUMERO '{peticion.rut}'")).fetchone()
            d = get_numero_to_dict(res)
            d["estado"] = "Cancelado"            
            conn.execute(text(f"EXEC CANCELAR_NUMERO '{peticion.rut}'"))
            conn.commit()
            return d
    
    def validar(self, peticion : Usuario):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"select nombre from dbDominion.dbo.persona where correo ='{peticion.usuario}' and clave='{peticion.password}'")).fetchone()
            print(res)
            if res:
                return True
            else:
                return False
                
    def validar_totem(self, peticion: Usuario):
        with self.__engine.connect() as conn:
            query = text(f"SELECT nombre FROM TOTEM.dbo.persona WHERE numDoc = '{peticion.usuario}' AND clave = '{peticion.password}'")
            res = conn.execute(query).fetchone()
            if res:
                return {'validation': True, 'nombre': res[0]}
            else:
                return {'validation': False, 'nombre': 'none'}
                
    def get_numeroApp(self, req: Rut):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_NUMERO '{req.rut}'")).fetchone()
      
            return get_numero_to_app(res)
            
    
    def validar_perfil (self, peticion: Usuario):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC Login_Totem '{peticion.usuario}' , '{peticion.password}'")).fetchone()
            print(res)
            if res:
                return {'validation' : True, 'perfil_id':res[2], 'nombre': res[1], 'estacion':res[3], 'modulo': res[4]}
            else:
                return {'validation' : False, 'perfil_id':'none', 'nombre': 'none', 'estacion':'none', 'modulo': 'none'}

    def login(self, usuario, contraseña):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC Login_Totem '{usuario}' , '{contraseña}'")).fetchone()
            if res:
                return {'validation' : True, 'perfil_id':res[2], 'nombre': res[1], 'estacion':res[3], 'modulo': res[4], 'rut':usuario}
            else:
                return {'validation' : False, 'perfil_id':'none', 'nombre': 'none', 'estacion':'none', 'modulo': 'none', 'rut':'none'}

    def registrar_token(self, rut, token) -> None:
        with self.__engine.connect() as conn:
            conn.execute(text(f"""INSERT INTO usuario_token VALUES (getdate(),'{rut}', '{token}')"""))
            conn.commit()

    def check_token(self, token_data : TokenData):

        with self.__engine.connect() as conn:
           res = conn.execute(text(f"""SELECT token
                                FROM USUARIO_TOKEN WHERE RUT='{token_data.user}'
                                order by fecha_creacion desc
                                """)).fetchone()
           ultimo_token = res[0]
           if ultimo_token==token_data.token:
               return True
        return False 
    
            
    def get_numeros_supervisor(self, req:Rut):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_TECNICOS_SUPERVISOR '{req.rut}'")).fetchall()
    
            return get_numeros_to_dict(res)

    def salida_numero(self, peticion : Rut):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_NUMERO '{peticion.rut}'")).fetchone()
            d = get_numero_to_dict(res)
            d["estado"] = "Completado"            
            conn.execute(text(f"EXEC MARCAR_SALIDA_RUT '{peticion.rut}'"))
            conn.commit()
            return d
            
    def get_reversa(self, rut:str):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_REVERSA '{rut}'")).fetchall()
            return reversa_to_dict(res)
        
    def get_reversa_pendiente(self, rut:str):
        with self.__engine.connect() as conn:
            res = conn.execute(text(f"EXEC GET_REVERSA '{rut}'")).fetchall()
            return reversa_to_dict(res, pendiente=True)    

    def update_TIF(self, tifs: listaTIF):

        with self.__engine.connect() as conn:
            query = f"UPDATE ESTADO_REVERSA SET impresion_tif = 1 where id in ({tifs.get_ids_impresion()})"
            query1 = f"UPDATE ESTADO_REVERSA SET entregado = 1, fechaEntrega = getdate() where id in ({tifs.get_ids_entrega()})"
            query2 = f"UPDATE ESTADO_REVERSA SET fuente = 1 where id in ({tifs.get_ids_fuente()})"
            
            conn.execute(text(query))
            conn.execute(text(query1))
            conn.execute(text(query2))            
            
            #res = conn.execute(text(f"""select distinct Rut_Tecnico 
            #                    from TOTEM.dbo.Estado_Reversa
            #                   where Id in ({tifs.get_ids_impresion()})""")).fetchone()
            #
            #query4 = f"exec TOTEM.dbo.LOG_DATA_TOTEM '{res[0]}', -1, 0, 2"
            #conn.execute(text(query4))
            conn.commit()
    
    