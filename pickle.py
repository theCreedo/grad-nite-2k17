import cPickle as pickle
emails = {
'''
Create a dictionary with keys of "graduate's name"
and values of "graduate's email"
Ex. 'Jon': 'jondoe@gmail.com'
'''
}
pickle.dump( emails, open( "emails.p", "wb" ))

values = {
'''
Creates a dictionary with keys of "graduate's name"
and values of list of "messages to graduates"
Ex. 'Jon':['You\'re a cool person', 'Please eat more veggies']
'''
}

pickle.dump( values, open( "values.p", "wb" ))