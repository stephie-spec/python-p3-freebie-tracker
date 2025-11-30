#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    # Setup database connection
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    print("---")

    # Get all instances
    companies = session.query(Company).all()
    devs = session.query(Dev).all() 
    freebies = session.query(Freebie).all()

    print(f"Companies: {companies}")
    print(f"Devs: {devs}")
    print(f"Freebies: {freebies}")

    print("\nrelationships")

    # Get specific instances by name
    alice = session.query(Dev).filter_by(name="Alice").first()
    bob = session.query(Dev).filter_by(name="Bob").first()
    joy = session.query(Dev).filter_by(name="Joy").first()
    google = session.query(Company).filter_by(name="Google").first()

    print(f"Alice: {alice}")
    print(f"Bob: {bob}")
    print(f"Joy: {joy}")
    print(f"Google: {google}")

    print(f"Alice's freebies: {alice.freebies}")
    print(f"Google's freebies: {google.freebies}")

    print(f"\nAlice's companies: {alice.companies}")
    print(f"Google's devs: {google.devs}")

    print("\nfreebie methods")
    if alice.freebies:
        freebie = alice.freebies[0]
        print(f"Freebie details: {freebie.print_details()}")

    print("\naggregate methods")
    oldest = Company.oldest_company(session)
    print(f"Oldest company: {oldest}")

    print(f"Alice received stickers: {alice.received_one('Stickers')}")
    print(f"Alice received hoodie: {alice.received_one('Hoodie')}")

    print(f"\ngive_away")
    if alice.freebies:
        freebie = alice.freebies[0]
        print(f"Before: Freebie belongs to {freebie.dev.name}")
        success = alice.give_away(bob, freebie)
        if success:
            session.commit()
            print(f"After: Freebie belongs to {freebie.dev.name}")
    else:
        print("No freebies available for give_away test")

    print(f"\ngive_freebie")
    new_freebie = google.give_freebie(joy, "Backpack", 30)
    session.add(new_freebie)
    session.commit()
    print(f"New freebie created: {new_freebie.print_details()}")

    print(f"\n---")
    print(f"Joy's freebies: {joy.freebies}")
    print(f"Google's freebies: {[f.item_name for f in google.freebies]}")

    # Start interactive session
    import ipdb; ipdb.set_trace()