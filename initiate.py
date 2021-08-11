import os
import atexit
import sys


import repository
from repository import Employee
from repository import Supplier


if __name__ == '__main__':
    DBExist = os.path.isfile('moncafe.db')
    if DBExist:
        os.remove('moncafe.db')
    repo = repository.Repository()
    repo.create_tables()
    inputfilename = sys.argv[1]
    with open(inputfilename) as inputfile:
        lines = inputfile.readlines()
        for line in lines:
            words = line.split(", ")
            if words[0] == 'E':
                words.remove(words[0])
                e = Employee(*words)
                repo.Employees.insert(e)
            elif words[0] == 'S':
                words.remove(words[0])
                repo.Suppliers.insert(Supplier(*words))
            elif words[0] == 'P':
                if words.__sizeof__() == 5:
                    q = words[4]
                else:
                    q = 0
                repo.Products.insert(repository.Product(words[1], words[2], words[3], q))
            elif words[0] == 'A':
                repo.Activities.insert(repository.Activitie(words[1], words[2], words[3], words[4]))
            elif words[0] == 'C':
                repo.Coffee_stands.insert(repository.Coffee_stand(words[1], words[2], words[3]))

atexit.register(repo._close)