import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 14: Object-Oriented Programming

    The concept of object-oriented programming is maybe one of the more computer sciency things that we will get into. Object-oriented programming (OOP) has been around since the 1960s and gained popularity most notably in the 1990s.

    As the Py4E text mentions, OOP provides another mechanism to abstract and compartmentalize the functions of your program, making it easier to work with large programs.

    One key concept in OOP is the idea of **classes** and **objects**. A class is a definition of a data format and methods that can be performed. For example, the string class defines the way text is stored in a string and the methods, like the `.upper()`, `.strip()`, etc., that the class can perform on strings. An instance of a class is called an object. So, something like `x='Hello'` creates an object, or instance of the string class, called `x` containing the data "Hello".

    Not that I think we need to talk on the level of a 6-year-old (or that I think the average 6-years-old would actually understand this article), I think Alexander Petkov's article [How to explain object-oriented programming concepts to a 6-year-old](https://www.freecodecamp.org/news/object-oriented-programming-concepts-21bb035f7260/) provides a nice introduction with helpful diagrams explaining the key concepts of OOP.

    Some of the key object-oriented programming concepts include:
    * **Encapsulation**: The concept that binds together the data and the functions that manipulate the data, and that keeps both safe from outside interference and misuse ([Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_programming#Encapsulation)).
      * The idea here is that by making an object to hold both the data associated with the object and the functions that act on the data, these data and functions are somewhat isolated from the rest of the code and can be managed as a discrete entity.

    * **Abstraction**: We've used this throughout the semester, trying to take a big problem, like driving to the grocery store and breaking it down into the component pieces. The parking in a parking space piece doesn't really need to know the details of the stopping at a red light on the way. Similarly, we don't need to know how a string object takes a string and returns an upper-case version of it--we just need to know that it can do this and how to use that method.

    * **Inheritance**: Objects are often very similar. Earlier we used the idea of parking a car in the parking lot is similar to parking a car at home and how you might use the same code and extend it to add the new features. With inheritance, we can create a class (a child class) that inherits the data definitions and methods from another (parent) class. The child class can then be extended to add new features.

    * **Polymorphism**: Is the condition of occurrence in different forms. Polymorphism is used at different levels and we've used polymorphic operators and functions:
    """)
    return


@app.cell
def _():
    # An example of operator polymorphism

    print(5 + 6)
    print("hi" + " everyone")
    return


@app.cell
def _():
    # An example of function polymorphism

    print(len("Go Gators!"))
    print(len([1,2,3]))
    print(len({'Name' : 'Matt', 'Food' : 'Chocolate'}))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.3 Using Objects
    """)
    return


@app.cell
def _():
    stuff = list()
    stuff.append('python')
    stuff.append('chuck')
    stuff.sort()
    print (stuff[0])
    print (stuff.__getitem__(0))
    print (list.__getitem__(stuff,0))

    # Code: http://www.py4e.com/code3/party1.py
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Py4E explains:
    > The first line constructs an object of type list, the second and third lines call
    the append() method, the fourth line calls the sort() method, and the fifth line
    retrieves the item at position 0.

    Py4E explains that the last three lines are equivalent in their results. The last two use the "dunder" methods--again, in general, these are not intended for people to use, but there isn't anything stopping you from doing so.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.4 Starting with programs and 14.5 Subdividing a problem

    These sections get back to the ideas of abstraction and how, we don't really care how BeutifulSoup parses links out of a page...all we need to know is how to use it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.6 Our first Python object

    This should really be called "Our first Python class" because to make an object, we need a class...
    """)
    return


@app.cell
def _():
    class PartyAnimal:
        x = 0

        def party(self):
            self.x = self.x + 1
            print('So far', self.x)
    _an = PartyAnimal()
    _an.party()
    _an.party()
    _an.party()
    # Code: http://www.py4e.com/code3/party2.py
    PartyAnimal.party(_an)
    return (PartyAnimal,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before we get too far, I think there is a clearer description of `self` in the online text [Object-Oriented Programming in Python](https://python-textbok.readthedocs.io/en/1.0/index.html) which has this in the [classes section](https://python-textbok.readthedocs.io/en/1.0/Classes.html#defining-and-using-a-class):

    > You may have noticed that both of these method definitions have `self` as the first parameter, and we use this variable inside the method bodies – but we don’t appear to pass this parameter in. This is because whenever we call a method on an object, *the object itself* is automatically passed in as the first parameter. This gives us a way to access the object’s properties from inside the object’s methods.
    >
    > In some languages this parameter is *implicit* – that is, it is not visible in the function signature – and we access it with a special keyword. In Python it is explicitly exposed. It doesn’t have to be called `self`, but this is a very strongly followed convention.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.7 Classes as types
    """)
    return


@app.cell
def _(PartyAnimal):
    _an = PartyAnimal()
    print('Type', type(_an))
    print('Dir ', dir(_an))
    print('Type', type(_an.x))
    print('Type', type(_an.party))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.8 Object lifecycle

    Python can do a lot of the work for use, creating objects and deleting them, but we *can* also write the `__init__` and `__del__` methods:
    """)
    return


@app.cell
def _():
    class PartyAnimal_1:
        x = 0

        def __init__(self):
            print('I am constructed')

        def party(self):
            self.x = self.x + 1
            print('So far', self.x)

        def __del__(self):
            print('I am destructed', self.x)
    _an = PartyAnimal_1()
    _an.party()
    _an.party()
    _an = 42
    print('an contains', _an)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.9 Multiple instances

    Just like we can have multiple instance (objects) of the string class, we can have multiple instances of our own classes:
    """)
    return


@app.cell
def _():
    class PartyAnimal_2:
        x = 0
        name = ''

        def __init__(self, nam):
            self.name = nam
            print(self.name, 'constructed')

        def party(self):
            self.x = self.x + 1
            print(self.name, 'party count', self.x)
    _s = PartyAnimal_2('Sally')
    _j = PartyAnimal_2('Jim')
    _s.party()
    _j.party()
    _s.party()
    return (PartyAnimal_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14.10 Inheritance

    Inheritance is the ability to create new classes (called the child class) that extend the features of and existing class (called the parent class).

    **Note** that for this example, the PartyAnimal class from section 14.9 is saved to a file in the current directory called [`party.py`](party.py) and is being imported.
    """)
    return


@app.cell
def _(PartyAnimal_2):
    class CricketFan(PartyAnimal_2):
        points = 0

        def six(self):
            self.points = self.points + 6
            self.party()
            print(self.name, 'points', self.points)
    _s = PartyAnimal_2('Sally')
    _s.party()
    _j = CricketFan('Jim')
    _j.party()
    _j.six()
    print(dir(_j))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Some additional examples

    Again, taking from the [Object-Oriented Programming in Python](https://python-textbok.readthedocs.io/en/1.0/index.html) text, here's a, perhaps more useful, example.
    """)
    return


@app.cell
def _():
    import datetime  # we will use this for date objects

    class Person:

        def __init__(self, name, surname, birthdate, address, telephone, email):
            self.name = name
            self.surname = surname
            self.birthdate = birthdate
            self.address = address
            self.telephone = telephone
            self.email = email

        def age(self):
            today = datetime.date.today()
            age = today.year - self.birthdate.year
            if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
                age = age - 1
            return age

    return Person, datetime


@app.cell
def _(Person, datetime):
    person = Person(
        "Jane",
        "Doe",
        datetime.date(1992, 3, 12), # year, month, day
        "No. 12 Short Street, Greenville",
        "555 456 0987",
        "jane.doe@example.com"
    )

    print(person.name)
    print(person.email)
    print(person.age())
    return


if __name__ == "__main__":
    app.run()
