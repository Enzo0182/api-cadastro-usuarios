from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schema, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Cadastro de Usuários")

# Dependência para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=schema.Usuario)
def criar_usuario(usuario: schema.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_por_email(db, usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.criar_usuario(db, usuario)

@app.get("/usuarios/", response_model=list[schema.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

@app.get("/usuarios/{usuario_id}", response_model=schema.Usuario)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}", response_model=schema.Usuario)
def atualizar_usuario(usuario_id: int, dados: schema.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.atualizar_usuario(db, usuario_id, dados)

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.deletar_usuario(db, usuario_id)
