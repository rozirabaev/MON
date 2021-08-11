from repository import repo


def print_employees():
    print('Employees')
    for tmp in repo.Employees.find_all('id'):
        print(tmp.__str__())

def print_suppliers():
    print('Suppliers')
    for sup in repo.Suppliers.find_all('id'):
        print(sup.__str__())

def print_activities():
    print('Activities')
    for tmp in repo.Activities.find_all('date'):
        print(tmp.__str__())

def print_product():
    print('Products')
    for tmp in repo.Products.find_all('id'):
        print(tmp.__str__())

def print_coffee_stands():
    print('Coffee stands')
    for tmp in repo.Coffee_stands.find_all('id'):
        print(tmp.__str__())

def emp_report():
    print("\nEmployees report")
    for emp in repo.Employees.find_all('name'):
        name=emp.name
        id=emp.id
        salary=emp.salary
        id_location=emp.coffee_stand
        act_list=repo.Activities.findByActiv(id)
        total=0
        for activ in act_list:
            quantity = activ.quantity
            price = float(repo.Products.findPrice(activ.product_id))
            total = total + (price * quantity * (-1))
        location=repo.Coffee_stands.findLocation(id_location)
        print(name+ " "+ str(salary) + " " + location + " " + str(total))

def act_report():
    report = repo.actReport()
    if len(report)>0 :
        print("\nActivities")
        for list in report:
            print(list)

def print_all():
    print_activities()
    print_coffee_stands()
    print_employees()
    print_product()
    print_suppliers()
    emp_report()
    act_report()


if __name__ == '__main__':
    print_all()

#atexit.register(repo._close)