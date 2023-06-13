from .secret import Secret
from .utils import get_session

def add_new_secret(new_secret: Secret):
    with get_session() as session:
        session.add(new_secret)
        session.commit()

    with get_session() as session:
        result = session.query(Secret).order_by(Secret.id.desc()).first()

    return result
    
def update_secret(secret_to_update: Secret, name:str, login: str, password: str, notes: str, master_password: str):
    secret_id = secret_to_update.id
    with get_session() as session:
        secret = session.query(Secret).get(secret_id)
        secret.update_data(name, login, password, notes, master_password)
        session.commit()

    with get_session() as session:
        result = session.query(Secret).get(secret_id)

    return result
        
def delete_secret(secret: Secret):
    with get_session() as session:
        session.delete(secret)
        session.commit()
        
def get_all_secrets():
    with get_session() as session:
        result = session.query(Secret).all()

    return result

def get_first_secret():
    with get_session() as session:
        result = session.query(Secret).first()

    return result