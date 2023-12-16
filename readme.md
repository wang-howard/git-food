# COS316 Final Project: GitFood #

## Group Members ##
* Tuan Dinh '25
* Nguyen Nguyen '25
* Howard Wang '24

## Running the App ##
1. Open your terminal and cd into the app directory (/git-food) and make sure you have pip installed
2. Activate the virtual env by executing this line in the terminal: `source venv/bin/activate`
3. Ensure the virtual environment is properly set up by executed: `pip install -r requirements.txt`
4. Set the following environment variables by executing in terminal: `export FLASK_APP=gitfood.py
export DB_URI=postgresql://git_food_user:uelFgIGe9GCTYYttir2XHNJ9Y4auBX4G@dpg-clrqa1cm7d1c73f483tg-a.ohio-postgres.render.com/git_food
export SEC_KEY=uelFgIGe9GCTYYttir2XHNJ9Y4auBX4G
export CLIENT_SECRET=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
export CALLBACK_URI=http://127.0.0.1:5553/callback'
5. Execute a local instance of the app: `python gitfood.py` (may need to use `python3` instead of `python`


