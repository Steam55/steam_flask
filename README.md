# BROKER 

## Installation of dependencies
All dependencies are in **requirements.txt** file.

```python
pip3 install -r requirements.txt
```
We recommend you to work in [virtual environment](https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4463278-travaillez-dans-un-environnement-virtuel)

## Usage
* Launch sql server:
  ```python
  sudo mysql -u root -p
  ```
  
* To launch virtual env
  ```python
  source env/bin/activate
  ```

* To stop virtual env
  ```python
  deactivate
  ```
  
* To launch the project (directory: steam) on all all addresses:
  ```python
  export FLASK_APP=project
  export FLASK_DEBUG=1
  flask run --host=0.0.0.0
  ```

* Initialize all table by typing:
```python
flask init-db
```
* If you are in developement launch:
```python
flask dev-migration
```
* If you are in production launch:
```python
flask prod-migration
```

* Add all packages to requirements.txt:
```
  pip freeze  > requirements.txt
```

* Launch `python run.py`
* Finally ot to `{{base_url}}/swagger` to see the documantation of the API
* Optional run
  ```python
  FLASK_APP=project flask api-generate
  ```
  to regenerate `static/swagger.json` file. You can catch errors due to your indent config

## Note
* A collection for SWAGGER is available at endpoint `/spec`

