
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CatalogItem

import random, string, sys

from xml.etree.ElementTree import  SubElement, Comment, Element, ElementTree, tostring, XML
from xml.dom import minidom


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg', 'tiff', 'bmp', 'svg'])


#user state debug block
def userStateDebug(login_session):
	print "User State:"
	print "username: %s"% login_session['username']
	print "securityState: %s"%login_session['securityState']
	print "email: %s"%login_session['email']




def createState():
	#create new state token to pass during post requests to mitigate XSS and CSRF attacks
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	return state



#Check that image file is valid and sanditize name for saving
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.')[1] in ALLOWED_EXTENSIONS


def prettify(elem):
	#Return a pretty-printed XML string for the Element.

	#rough_string = tostring(elem, 'utf-8')    #--alt 1
	rough_string = tostring(elem, method="xml")   #--alt 2
	#print "Type: %s"%type(rough_string)
	#print "xmlstring: %s"%rough_string
	#print "xmlstring 2: %s"% XML(tostring(elem, 'utf-8'))
	
	#reparsed = minidom.parseString(rough_string)   #--alt 1
	#reparsed = minidom.parse(rough_string)


	#return reparsed.toprettyxml(indent="\t") #-- alt 1
	#return reparsed.toxml()
	return rough_string    #-- alt 2





# User Helper Functions
def createUser(session, login_session):
	newUser = User(name=login_session['username'], email=login_session[
				   'email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id


def getUserInfo(session, user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user


def getUserID(session, email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None


		#<class 'xml.etree.ElementTree.Element'>
#xmlstring:<Catalog>New one<Category Name /><Image Name /><Description>This is the first item</Description><Item Name>Item 1</Item Name><Image Name /><Description>This is the second item</Description><Item Name>Item 2</Item Name><Category Name /><Image Name /><Description>This is the third item</Description><Item Name>Item 3</Item Name><Image Name /><Description>This is the fourth item</Description><Item Name>Item 4</Item Name><Image Name /><Description>glasses cat</Description><Item Name>sun</Item Name><Image Name /><Description>tweedledee</Description><Item Name>sunglasses sunshine</Item Name><Category Name /><Image Name /><Description>is banana</Description><Item Name>this thing</Item Name><Image Name>index.jpeg</Image Name><Description>man</Description><Item Name>banan</Item Name></Catalog>
