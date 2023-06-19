# PasswordManager
Project for Scripting Languages laboratory course at Wrocław University of Sciece and Technology.

PasswordManager allows user to securely store secrets in database using simple GUI.

It uses AES for encryption, PyQt5 for GUI and sqlite3 for database.

# Using the application
## Cloning the project
```bash
git clone https://github.com/kubawen10/PasswordManager.git
cd PasswordManager
```

## Running as a script
You can run the application directly as a script 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

## Installation guide for Ubuntu
You can install the application on your machine.

Instalation was tested only on ubuntu. If you want to install it on other systems feel free to modify the files as you need.

### Venv and requirements
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Installing fpm
In order to create a package you need to install fpm
```bash
sudo apt update
sudo apt install ruby
gem install fpm --user-install
fmp --version
```

If fmp --version doesnt work, you need to add ruby to the PATH, change variables in <> properly
```bash
export PATH="/home/<user>/.local/share/gem/ruby/<ruby-version>/bin:$PATH"
```

### Building python app using PyInstaller

```bash
pyinstaller password-manager.spec
```

### Building package structure
```bash
./build-package-structure.sh
```

### Building package
```bash
fpm
```

### Instaling package
```bash
sudo dpkg -i password-manager.deb
```

# Using copy to clipboard feature
Sometimes in order to use copy to clipboard you have to install xsel or xclip