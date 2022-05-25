from sqlalchemy import create_engine

engine = create_engine('postgresql://mwskkfmznktnbk:2bdafd106324e3b963f350fddeef809320718f86ad8e2500f664d528c10dfe30@ec2-52-204-195-41.compute-1.amazonaws.com:5432/d1665plnmsmfoi', echo=False, pool_pre_ping=True)
