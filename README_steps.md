Open a folder (DEVINAI) and go to agent mode

Paste this in the chat then
```
Create a modern full-stack Expense Tracker application.

Tech stack:
- React + TypeScript frontend
- FastAPI backend
- SQLite database

Features:
- User authentication
- Add, edit, delete expenses
- Monthly dashboard
- Category filtering
- Responsive UI

First, create a development plan and then begin implementing the project step by step.

```
![images\chat.png](images\chat.png)

![images\p1.png](images\p1.png)

![images\p2.png](images\p2.png)

![images\p3.png](images\p3.png)



### Giving real task

Once the initial files are created, let's give it another task

"
The application works, but now I'd like to improve it.

Please analyze the entire project first.

Then identify:
- code duplication
- security issues
- performance improvements
- missing tests
- better folder structure

Don't modify anything yet.
Create a report first."

![images\p4.png](images\p4.png)


![images\p5.png](images\p5.png)

### Then ask for CodeMap
Then we can paste this :

Create a visual explanation of how this project is organized.

Include:
- frontend
- backend
- database
- authentication
- API flow

These files are generated now:

![images\p6.png](images\p6.png)


### Use DeepWiki

Go to main.py and then press Ctrl+Shift and press on a method. For example, here I pressed on health_check() method.

![images\p8.png](images\p8.png)


DeepWiki explains

- why it exists
- who calls it
- where it's used
- related architecture
![images\p9.png](images\p9.png)

We can also use expenses.py file's delete_expense method.
Note: File path is backend\app\routes\expenses.py

Now go back to agent mode, and paste this

```
@expenses.py

Explain how expense creation works and where I should add recurring expenses.
```
![images\p10.png](images\p10.png)

This is the output:
![images\p11.png](images\p11.png)


### Supercomplete

Start typing

```
def calculate_monthly_summary(
```

![images\p12.png](images\p12.png)


And we get suggestions for the code.

![images\suggestion.png](images\suggestion.png)

Supercomplete predicts the entire coding intention instead of only the next word.


### Refactoring

Now paste this 

```
Refactor the backend.

Goals:

- reduce duplicated code
- improve readability
- keep the same functionality
- don't break existing APIs
```

![images\p13.png](images\p13.png)


### Quick review

Paste this:

```
Review every file you modified.

Find:

- bugs
- edge cases
- performance problems
- security issues

Do not fix them yet.
```

![images\p14.png](images\p14.png)


### Testing

Paste this:

```
Write comprehensive tests for every API endpoint.

Run the tests.

Fix failures until everything passes.

```
![images\p15.png](images\p15.png)

![images\p16.png](images\p16.png)


So, Notice that Devin isn't only writing code.


It is

- exploring the repository
- executing commands
- installing packages
- creating files
- fixing errors
- retrying failed commands
- reasoning over the whole project



That's the difference between autocomplete and an autonomous software engineering agent.


