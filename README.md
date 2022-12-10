<!-- README TOP -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">GoDelv</h3>

  <p align="center">
    An online delivery service for all of your delivery needs!
    <br />
    <a href="https://github.iu.edu/cuhoward/p565-team22-godelv"><strong>Explore the project »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#file-structure">File Structure</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

While there are many different delivery services out there that all offer their own web applications, GoDelv is the best of them all. GoDelv combines all of those separate deilvery services into one web service. GoDelv lets customers, delivery managers, and delivery drivers handle all of their business on one website. Customers can place and track their orders on delivery services added by delivery managers delivered by delivery drivers. Save the headache, let GoDelv make it easy.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

These are the major frameworks that we used in the development of GoDelv.

1. HTML
2. CSS
3. Javascript
4. jQuery
5. AJAX
6. Python
7. Flask
8. Jinja
9. MySQL

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Listed in this section are the prerequisites and installation instructions for this project.

### Prerequisites

* Python 3.9

### Installation

1. Clone the repo
   ```sh
   git clone https://github.iu.edu/cuhoward/p565-team22-godelv
   ```
2. Open the repo as a Python project
3. Create a virtual environment in the repo
   ```sh
   py -m venv venv
   ```
4. Run venv/Scripts/activate
   ```sh
   venv/Scripts/activate
   ```
5. You should now see (venv) to the left side of your command line
6. Install requirements
   ```sh
   pip install -r requiremnts.txt
   ```
7. Run "app.py"

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FILE STRUCTURE -->
## File Structure

The file structure of your project should look something like this:

```
.
├── Procfile
├── app.py
├── godelv
│   ├── __init__.py
│   ├── forms
│   │   ├── AddServiceForm.py
│   │   ├── CreateShipmentForm.py
│   │   ├── DelegateOrdersToDriver.py
│   │   ├── LoginForm.py
│   │   ├── PasswordResetForm.py
│   │   ├── RegistrationForm.py
│   │   ├── TrackbyIDForm.py
│   │   ├── UpdatePasswordForm.py
│   │   └── UpdateShippmentStatusLocationForm.py
│   ├── routes.py
│   ├── static
│   │   ├── main.css
│   │   └── trackingbyidresult.css
│   └── templates
│       ├── addservice.html
│       ├── adminhome.html
│       ├── assigndriverfororder.html
│       ├── createshipment.html
│       ├── customer_home.html
│       ├── delegateorders.html
│       ├── deliverydriver_home.html
│       ├── display_username.html
│       ├── home.html
│       ├── layout.html
│       ├── login.html
│       ├── map.html
│       ├── password_reset.html
│       ├── payment.html
│       ├── register.html
│       ├── searchandFilter.html
│       ├── trackbyid.html
│       ├── trackingbyidresult.html
│       ├── two_factor_setup.html
│       ├── updateShippmentLocation.html
│       ├── updateShippmentStatusLocation.html
│       └── update_password.html
├── godelv.sql
├── requirements.txt
└── venv
```

<!-- LICENSE -->
## License

Currently not distributed under any license.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

GoDelv - godelvcompany@gmail.com

Project Link: https://github.iu.edu/cuhoward/p565-team22-godelv

<p align="right">(<a href="#readme-top">back to top</a>)</p>
