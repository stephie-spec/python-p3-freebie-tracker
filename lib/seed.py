#!/usr/bin/env python3

from models import Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_database():
    # Clear existing data
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()
    
    # Create companies
    google = Company(name="Google", founding_year=1998)
    microsoft = Company(name="Microsoft", founding_year=1975)
    apple = Company(name="Apple", founding_year=1976)
    
    session.add_all([google, microsoft, apple])
    session.commit()
    
    # Create devs
    alice = Dev(name="Alice")
    bob = Dev(name="Bob")
    joy = Dev(name="Joy")
    
    session.add_all([alice, bob, joy])
    session.commit()
    
    # Create freebies
    freebie1 = Freebie(item_name="T-shirt", value=15, dev_id=alice.id, company_id=google.id)
    freebie2 = Freebie(item_name="Stickers", value=5, dev_id=alice.id, company_id=microsoft.id)
    freebie3 = Freebie(item_name="Water Bottle", value=20, dev_id=bob.id, company_id=apple.id)
    
    session.add_all([freebie1, freebie2, freebie3])
    session.commit()
    
    print("Database seeded")

if __name__ == "__main__":
    seed_database()