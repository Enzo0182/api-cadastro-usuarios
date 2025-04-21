from sqlalchemy.orm import Session
import models, schema
from bcrypt import hashpw, gensalt, checkpw

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def listar_usuarios(db: Session):
    return db.query(models.Usuario).all()

def criar_usuario(db: Session, usuario: schema.UsuarioCreate):
    senha_hash = hashpw(usuario.senha.encode('utf-8'), gensalt())
    db_usuario = models.Usuario(nome=usuario.nome, email=usuario.email, senha=senha_hash.decode('utf-8'))
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def atualizar_usuario(db: Session, usuario_id: int, dados: schema.UsuarioCreate):
    usuario = get_usuario(db, usuario_id)
    if usuario:
        usuario.nome = dados.nome
        usuario.email = dados.email
        usuario.senha = hashpw(dados.senha.encode('utf-8'), gensalt()).decode('utf-8')
        db.commit()
        db.refresh(usuario)
        return usuario
    return None

def deletar_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
        return {"msg": "Usuário deletado"}
    return {"msg": "Usuário não encontrado"}
