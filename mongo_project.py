import pymongo
import os
if os.path.exists("env.py"):
    import env

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "myFirstMDB"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a Record")
    print("2. Find a Record by Name")
    print("3. Edit a Record")
    print("4. Delete a Record")
    print("5. Exit")

    option = input("Enter Option: ")
    return option

def get_record():
    print("")
    first = input("Enter First Name > ")
    last = input("Enter Last Name > ")

    try:
        doc = coll.find_one({'first': first.lower(), 'last': last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! no results found.")

    return doc


def add_record():
    print("")
    first = input("Enter First Name > ")
    last = input("Enter Last Name > ")
    dob = input("Enter Date of Birth > ")
    gender = input("Enter Gender > ")
    hair_colour = input("Enter Hair Colour > ")
    occupation = input("Enter Occupation > ")
    nationality = input("Enter Nationality > ")

    new_doc = {'first': first.lower(), 'last': last.lower(), 'dob': dob, 'gender': gender,
               'hair colour': hair_colour, 'occupation': occupation, 'nationality': nationality}

    try:
        coll.insert(new_doc)
        print("")
        print("Document Inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ":" + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc ={}
        print("")
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                if update_doc[k] == "":
                    update_doc[k] = v
        
        try:
            coll.update_one(doc, {'$set': update_doc})
            print("")
            print("Document Updated.")
        except:
            print("Error accessing the database")

def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ":" + v.capitalize())
        
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")

        if confirmation.lower() == 'y':
            try:
                coll.delete_one(doc)
                print("Document Deleted!")
            except:
                print("Error accessing the databse")
        else:
            print("Document not deleted")



def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("invalid option")
        print("")


conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

main_loop()
