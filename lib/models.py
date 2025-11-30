from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    freebies = relationship('Freebie', backref='company')
    devs = relationship('Dev', secondary='freebies', viewonly=True)

    def give_freebie(self, dev, item_name, value):
        """Create a new Freebie for this company and given dev"""
        freebie = Freebie(
            item_name=item_name,
            value=value,
            dev_id=dev.id,
            company_id=self.id
        )
        return freebie

    @classmethod
    def oldest_company(cls, session):
        """Return the Company instance with the earliest founding year"""
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    freebies = relationship('Freebie', backref='dev')
    companies = relationship('Company', secondary='freebies', viewonly=True)

    def received_one(self, item_name):
        """Return True if dev has any freebie with given item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        """Give a freebie to another dev if it belongs to current dev"""
        if freebie.dev_id == self.id:
            freebie.dev_id = other_dev.id
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def __repr__(self):
        return f'<Freebie {self.id}: {self.item_name}>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"