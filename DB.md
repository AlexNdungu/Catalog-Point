## CatalogPoint DataBase
**DataBase** -  is an organized collection of data stored in a computer system and usually controlled by a database management system (DBMS).

### Django And DataBase

**Django** offers a powerful and flexible **Object-Relational Mapping (ORM)** system that simplifies the interaction with databases.

- Database tables are represented as Python classes, and each table row becomes an instance of a class.

**Django Model** - A model is a Python class that defines the structure of a database table.

**Django Migrations** - Migrations copy the **models(classes)** into the database as **tables(relations)**.

```
python manage.py makemigrations
python manage.py migrate
```

**Querying the Database** - Django ORM offers a powerful querying API for data retrieval, filtering, and manipulation.

*Example*
```
# Get a book using id
Book.objects.get(book_id = pk)
```

**Django Relationships**

- **One-to-One** : relationship establishes a link between two tables where each row in one table **corresponds to exactly one row** in another table, and vice versa. 

- **One-to-Many** : A model can have a **ForeignKey** to another model, establishing a one-to-many relationship.

- **Many-to-Many** : You can define a **ManyToManyField** to create a many-to-many relationship between two models.