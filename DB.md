## CatalogPoint DataBase

**DataBase** -  is an organized collection of data stored in a computer system and usually controlled by a database management system (DBMS).

### Django And DataBase
---

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

## CatalogPoint Models

### Profile
---

**user**
- This attribute establishes a **one-to-one relationship** between the **Profile model** and the built-in **User model** provided by Django’s authentication system.
- Each **Profile** instance is associated with **exactly one User**, and vice versa.

**profile_id** - This attribute represents the primary key of the Profile model (automatically generated).

**full_name** - A character field (string field) named full_name. This is the field that stores the full name of the user.

**bio** - A text field for storing longer text, such as a user’s biography.

**company** - A character field for representing the company or organization associated with the user.

**location** - A text field to store the user’s location (e.g., city, country).

**secondary_email** - A URL field for storing secondary email addresses or URLs.

**website** - A URL field to store the user’s personal website or blog.

**profile_pic** - An image field for uploading profile pictures.

---

### Category
---

**category_id** - An automatically generated primary key (integer) for each category.

**category_name** - A character field (string) to store the name of the category.

**category_description** - A text field for a longer description of the category.

**followers**

- A **many-to-many relationship** field that links the Category model with the Profile model.

- Each category can have multiple followers (users who appreciate the category).

---

### Book
---

**book_id** - An automatically generated primary key (integer) for each book.

**book_name** - A character field (string) to store the name of the book.

**book_author** - A character field for representing the author’s name.

**book_description** - A text field for a longer description of the book.

**book_category** - A **foreign key relationship** with the Category model. Each book is associated with a specific category.

**book_cover** - An image field for uploading the book cover image.

**book_pages** - An integer field for storing the number of pages in the book.

**all_copies** - An integer field representing the total number of copies of the book.

**given_copies** - Another integer field for tracking the number of copies given to users.

**users_who_have** - A many-to-many relationship with the Profile model. Represents the users who have the book.