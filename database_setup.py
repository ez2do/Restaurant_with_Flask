import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#declare a mapping from python defined class to database table
Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)


class MenuItem(Base):
	__tablename__ = 'menu_items'
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(20))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		return {
		'id': self.id,
		'name': self.name,
		'course': self.course,
		'description': self.description,
		'price': self.price,
		'restaurant_id': self.restaurant_id,
		'restaurant': self.restaurant.name
		}
	
		
#Insert at the end
#connect to the database
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)