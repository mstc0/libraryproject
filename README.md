## About The Project

Games library project as my first fully fledged assignment during my Python learning course.
Project contains basic account funcionalities, homepage featuring added games, list of added games, user profiles with working friend lists, wishlist, cart, admin panel, list of games pulled from Steam API.

<details>
  <summary>Project Screenshots</summary>
  <IMG src="https://i.imgur.com/rudtgj9.png"/>
  <IMG src="https://i.imgur.com/Zww6D79.png"/>
  <IMG src="https://i.imgur.com/7kN9OIs.png"/>
  <IMG src="https://i.imgur.com/1qIQnZq.png"/>
  <IMG src="https://i.imgur.com/ulRTqAo.png"/>
  <IMG src="https://i.imgur.com/bv70tlY.png"/>
  <IMG src="https://i.imgur.com/hy3sJWy.png"/>
</details>


### Built With

* [![Python][Python]][Python-url]
* [![Django][Django]][Django-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]



### Prerequisites

* Python 3.10

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mstc0/libraryproject.git
   ```
3. Install requirements.txt
    ```sh
    pip install -r requirements.txt
    ```
2. Migrate Django
   ```sh
   py manage.py migrate
   ```
3. Create superuser
   ```sh
   py manage.py createsuperuser
   ```

### Usage
  ```sh
   py manage.py createsuperuser
   ```

<!-- USAGE EXAMPLES -->
## Steam API

To populate list of Steam games visit endpoint with superuser account
   ```sh
   /manage/admin/apigames
   ```
This will pull list of products from Steam library. Selecting games from populated list will attempt to pull more detailed info from Steam, record will be deleted if it cannot.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://www.djangoproject.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
