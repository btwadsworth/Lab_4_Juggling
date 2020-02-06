import sqlite3

file_db = 'jugglers_db.sqlite'


def main():
    print('Chainsaw Juggling Record Holders as of July 2018')
    create_table()
    while True:
        response = menu()
        if response == '1':
            add()
        elif response == '2':
            search()
        elif response == '3':
            update()
        elif response == '4':
            delete()
        elif response == '5':
            break
        else:
            print('Invalid choice.\n')


def create_table():
    create_table_sql = 'create table if not exists juggling (name text, country text, record integer)'
    conn = sqlite3.connect(file_db)
    conn.execute(create_table_sql)
    data = conn.execute('select * from juggling')
    if data is None:
        conn.execute('insert into juggling values ("Janne Mustonen", "Finland", 98)')
        conn.execute('insert into juggling values ("Ian Stewart", "Canada", 94)')
        conn.execute('insert into juggling values ("Aaron Gregg", "Canada", 88)')
        conn.execute('insert into juggling values ("Chad Taylor", "USA", 78)')
    conn.commit()
    conn.close()


def menu():
    print()
    print('1: Add New Record')
    print('2: Search By Name')
    print('3: Update Record')
    print('4: Delete Record')
    print('5: Exit')
    response = input('Choice: ')
    return response

# Add a new record holder to the table
def add():
    name = input('Name: ')

    country = input('Country: ')
    
    record = input('Number of Catches: ')
    while not record.isdigit():
        print('Enter Numbers Only')
        record = input('Number of Catches')
    
    conn = sqlite3.connect(file_db)
    conn.execute('insert into juggling values ("%s", "%s", %s)' % (name, country, record))
    conn.commit()
    conn.close()

# Search for a record holder
def search():
    name = input('Name: ')
    conn = sqlite3.connect(file_db)
    data = conn.execute('select * from juggling where name like "%s"' % (name + '%'))
    if data is None:
        print('There are no record holders with that name.')
    else:
        for item in data:
            print(item)
    conn.close()

# Update the number of catches for a record holder
def update():
    name = input('Name: ')
    conn = sqlite3.connect(file_db)
    data = conn.execute('select * from juggling where name like "%s"' % (name + '%'))
    if data is None:
        print('There are no record holders with that name.')
    else:
        catches = input('New number of catches: ')
        while not catches.isdigit():
            catches = input('New number of catches: ')
        for item in data:
            name = item[0]
        conn.execute('update juggling set catches = %s where name like "%s"' % (catches, name))
        conn.commit()
    conn.close()

# Delete a record holder
def delete():
    name = input('Name: ')
    conn = sqlite3.connect(file_db)
    data = conn.execute('select * from juggling where name like "%s"' % (name + '%'))
    if data is None:
        print('There are no record holders with that name.')
    else:
        for item in data:
            name = item[0]
        answer = input('Are you sure you want to delete the record for %s? (Y/N)' % name)
        while answer.upper() != 'Y' and answer.upper() != 'N':
            answer = input('Are you sure you want to delete the record for %s? (Y/N)' % name)
        if answer.upper() == 'Y':
            conn.execute('delete from juggling where name = "%s"' % name)
            conn.commit()
    conn.close()


main()