from sqlalchemy import create_engine

engine = create_engine('?', echo=False, pool_pre_ping=True)
