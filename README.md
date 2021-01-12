# wgu_capstone

---

This started as my capstone project at WGU. It is blog sit that provides CRUD opperation to users. Users can register, manage their accounts, create post and comments and threads. It uses the Flask framework with Handlebars to build UI templates with an SQLite database. Search functionalty was added later using ElasticSearch.

### Running Program

---

To get started running the program clone the app with `git clone <what ever branch you want to start with>` and the `cd wgu_capstone`. Then create a virtural envirnment with by running `python3 -m venv <venv_name>` then `source <venv_name>/bin/activate`. In your terninal window you should you should see `(<venv_name)` to the left of your terminal prompt. Once inside the virtural envirnment run `pip3 install -r requirnments.txt`. This command uses `pip3` to `install` the requirnment for the project listed in the `requirnments.txt` the `-r` flag is for recursive which has pip install all the requirnents listed.

Next you will need to create a file called dictionary_profile.py with `touch dictionary_profile.py` then add this to the contents
``` python
email_profile= {
    'EMAIL_USER':  "<emai>,
    'EMAIL_PASS': "<email_pass>"
    }

# set app key and tell where the sqlite db will be created.
app_key = dict({
    'SECRET_KEY': "<key>",
    'DB_URI': "sqlite:///site.db"
    })

ELASTICSEARCH_URL=dict({
'URL':"<location>"
    # if the instance is local
    # 'URL': "http://127.0.0.1:9200"
})
```

Once envirnment is set launch the site by navigating to root directory and run `python3 run.py`.

There is an issue installing the for some reason PyGObject==3.34.0 with the rest of the requirnments so it will need to be installed seperatly with `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0`.
