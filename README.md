
![Logo](https://davidloera-flask.info/static/logo-flask-app.png)


# FlaskyLinux Command Hub

This project was created solely for demonstrative purposes, aimed at showcasing the following functionalities:

1. Basic administration of a 'Linux/Debian 12' server.
2. Addition, editing, and deletion of users and groups in Linux using 'bash'.
3. Utilization of a 'MySQL' database to log actions such as user addition and editing, as well as to store server resources for monitoring purposes.
4. Terminal output to enable user management from the application using the 'root' user.
5. Server monitoring through logs or graphical representations of the server's state.
6. Use of unit tests to verify potential cases in the functions.

####

As mentioned earlier, this project was created purely for demonstrative purposes. Therefore, the use of the root user and leaving it accessible publicly was solely to simplify the concept of 'CRUD in BASH'.


## Tech Stack

**Client:** Bootstrap 5, JQuery, FontAwesom, Chart.js

**Server:** Python, Flask, MySql, Ajax, Bcrypt, Subprocess


## FAQ

#### How can I add/edit/remove a user from the server?

After accessing the "login" view, in our "home" view, we will find a small administration panel where we can add new users, edit them, and delete them. Right there, we format the registered data to generate new users and groups in Linux. For example, if we add a user named "#Rodrigo Lopez 56," the server will format the data to "rodrigo-lopez" to avoid problems when saving or editing the user from bash and thus follow the format that users and groups in Linux use.

#### What actions can I perform in the "terminal"?

The "terminal" view shows us an input where everything we execute there is done as "root". We can do practically anything except open applications since this view is only responsible for showing terminal outputs. We can install packages, update packages, create directories, access them, etc.

#### How can I view the performance and activity of the server?

In the "resources" and "logs" views, we can see the server's resource usage and at the same time textual outputs such as warnings or actions that have been performed.


## Terminal

The terminal input in the 'terminal' view works by sending input to the server terminal as follows: 'command' + Enter.
In the following example, we will run a bash script to display the users on the server with their respective groups:

```bash
  for user in $(cut -d: -f1 /etc/passwd); do groups $user; done
```

Alternatively, we can run the same script stored at the following path to view the users and groups:

```bash
  ./bash/show-users-and-groups.sh
```

### Output:
```bash
  root : root
  a21110121 : a21110121 adm dip video plugdev
  alondra : alondra guest-user
  hector-in : hector-in guest-user
  ihector : ihector standard-user
  test-user : test-user standard-user
  benjamin-cor : benjamin-cor guest-user
  david : david guest-user
  david-root : david-root root sudo
```


## Internal usage/Examples

In this section, I show how I added users in bash from Python using "subprocess".

```python
import subprocess

# Make a new user on the system
try:
    # Using 'useradd' to make a new user
    subprocess.run(['useradd', '-m', '-p', password, '-G', group, user_name], check=True)
    
    # Changing the shell for the user
    subprocess.run(['chsh', '-s', '/bin/bash', user_name])

    # Granting "root" permissions if the user was made as root
    if group == 'root':
        add_sudo_user(user_name)
    
except subprocess.CalledProcessError as e:
    logging.error('Error adding the user: %s', str(e))
    flash('Error adding the user. Please try again.', 'danger')


# Function to add a user to the "root" group
def add_sudo_user(user_name):
    try:
        # Add user to the sudo group
        subprocess.run(['usermod', '-aG', 'sudo', user_name], check=True)

        # Open the sudoers file in write mode
        with open('/etc/sudoers', 'a') as f:
            # Write the line to grant user permissions
            f.write(f'{user_name} ALL=(ALL:ALL) NOPASSWD: ALL\n')
        print(f'Sudo permissions granted to {user_name} successfully.')
    except Exception as e:
        print(f'Error granting sudo permissions to {user_name}: {e}')
```


## Server Resources

In the "resources" view, we can visualize the server's resource performance: (CPU Usage, Memory Usage, Disk Usage, Network Traffic In, Network Traffic Out). Using Ajax to query the database for saved resources and displaying them with Chart.js.

![server-resources](https://github.com/DavidAr55/bash-users/assets/78278095/08e0aae4-92bf-4ed8-9d90-56e6bb6ee58b)

## Author

- [@DavidAr55](https://www.github.com/DavidAr55)
