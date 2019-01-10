from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

#set up to read the data base
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

#home page, list of menu
@app.route('/', methods = ['GET', 'POST'])
def HomePage():
	if request.method == 'POST':
		option = request.form['option']
		if option == 'restaurants':
			return redirect(url_for('ShowRestaurants'))
		else:
			return redirect(url_for('ShowMenu'))

	else:
		return render_template('homePage.html')

@app.route('/restaurants')
def ShowRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/menus')
def ShowMenu():
	menus = session.query(MenuItem).all()
	return render_template('menu.html', menus = menus)

#show menu of a restaurant
@app.route('/restaurants/<int:restaurantID>/menu')
def ShowRestaurantMenu(restaurantID):
	restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()
	return render_template('restaurant_menu.html', 
		restaurant = restaurant, menus = menu_items)

#add new menu item
@app.route('/menu/new/<int:restaurant_id>', methods = ['GET', 'POST'])
def NewMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		menu_name = request.form['name']
		new_menu = MenuItem(name = menu_name, restaurant = restaurant)
		session.add(new_menu)
		session.commit()
		return redirect(url_for('ShowRestaurantMenu', restaurantID = restaurant.id))

	# GET request
	else:
		return render_template('addMenu.html', restaurant = restaurant)


#edit menu item
@app.route('/menu/edit/<int:restaurant_id>/<int:menu_id>', methods = ['GET', 'POST'])
def EditMenu(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		new_name = request.form['new_name']
		menu.name = new_name
		session.add(menu)
		session.commit()
		return redirect(url_for('ShowRestaurantMenu', restaurantID = restaurant.id))

	else:
		return render_template('edit.html', restaurant = restaurant, menu = menu)

@app.route('/menu/delete/<int:restaurant_id>/<int:menu_id>', methods = ['POST', 'GET'])
def DeleteMenu(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		option = request.form['option']
		if option == 'yes':
			session.delete(menu)
			session.commit()
		return redirect(url_for('ShowRestaurantMenu', restaurantID = restaurant.id))

	else:
		return render_template('delete.html', restaurant = restaurant, menu = menu)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '', port = 6969)