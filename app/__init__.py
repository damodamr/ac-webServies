from .views import app
from .models import graph

#nodes = [ ('User','username'), ('STATE','description'), ('EVENT','description'), ('ROLE', 'description'), ('ACTIVITY', 'description'), ('OBJECT', 'description')]

#for label, property in nodes:
    #try:
        #graph.schema.create_uniqueness_constraint(label, property)
    #except:
        #continue