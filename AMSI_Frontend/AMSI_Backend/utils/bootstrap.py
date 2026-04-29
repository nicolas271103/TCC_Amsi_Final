import logging
import sys
import os

# Adiciona o diretório raiz ao path para encontrar models e database
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario import Usuario, CargoEnum, AcessoEnum
from utils.auth_utils import hash_senha
from utils.frequentes import configure_logging, colorir

def garantir_admins_iniciais():
    configure_logging()
    db: Session = SessionLocal()
    
    ADMINS_INICIAIS = [
        {
            "email": "opedroschvartz@gmail.com",
            "nome": "Pedro Schvartz",
            "senha_plana": "123",
            "cargo": CargoEnum.Diretor,
            "perfil_de_acesso": AcessoEnum.Administrador
        },
        {
            "email": "nicolasmoreira206profissional@gmail.com",
            "nome": "Nicolas Moreira",
            "senha_plana": "123",
            "cargo": CargoEnum.Diretor,
            "perfil_de_acesso": AcessoEnum.Administrador
        }
    ]
    
    try:
        for admin_data in ADMINS_INICIAIS:
            usuario_existente = db.query(Usuario).filter(
                Usuario.email == admin_data["email"],
                Usuario.exclusao == None
            ).first()
            
            if not usuario_existente:
                print(colorir(cor="azul", texto=f"🚀 Criando admin: {admin_data['email']}"))
                novo_admin = Usuario(
                    email=admin_data["email"],
                    nome=admin_data["nome"],
                    senha=hash_senha(admin_data["senha_plana"]),
                    cargo=admin_data["cargo"],
                    perfil_de_acesso=admin_data["perfil_de_acesso"],
                    notificacao=True,
                    bloqueado=False,
                    primeiro_acesso=True
                )
                db.add(novo_admin)
            else:
                print(colorir(cor="verde", texto=f"✔ Admin {admin_data['email']} já existe."))
        
        db.commit()
        print(colorir(cor="verde", texto="\n✨ Processo de semente concluído com sucesso."))
    
    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao executar bootstrap: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    garantir_admins_iniciais()