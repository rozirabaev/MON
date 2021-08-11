import sys

import printdb

import repository
from  repository import repo



if __name__ == '__main__':
    inputfilename = sys.argv[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            words = line.split(", ")
            last_quantity = int(repo.Products.findByProd(words[0])[0])
            if int(words[1]) > 0:
                repo.Activities.insert(repository.Activitie(words[0], words[1], words[2], words[3]))
                new_quantity = (int(words[1])+last_quantity)
                repo.Products.updrage_quan(new_quantity, float(words[0]))
            elif int(words[1]) < 0:
                if last_quantity >= (-1)*int(words[1]):
                    repo.Activities.insert(repository.Activitie(words[0], words[1], words[2], words[3]))
                    new_quantity = (last_quantity+float(words[1]))
                    repo.Products.updrage_quan(new_quantity, float(words[0]))
    printdb.print_all()



