# Microearthquake Data Analytics Web App

<div align='center'>
    <img src='documentation/demo.gif'>
</div>

## Overview

The **Microearthquake Data Analytics Web App** is a web application built professionally with **Django** designed specifically for internal development and operational use. 

This dashboard allows for the analysis and visualization of microearthquake data during routine monitoring. 

Utilizing **Plotly JS**, it provides swift and interactive visualizations, including various plotting capabilities for efficient data analysis.

---

## Architecture and Scheme
<div align='center'>
    <img src='documentation/schematic.png'>
</div>
---

## Features
- Multi-site feature makes it easier for the  subsurface department, stakeholders, or project owner to monitor their assets.
- Secure and robust Authentication and Authorization (role-based feature).
- Powerful yet simple Admin page.
- Interactive visualizations of microearthquake events.
- Integration with a PostgreSQL/PostGIS database for effective geographical data handling, managing, and ensuring security.
- Automated data querying and processing using Django ORM, Pandas, and NumPy.
- Powerful backend engine for data cleansing and processing.
- JavaScript (fetch API) front-end interactions for real-time data updates and analysis.
- User-friendly interface for managing and navigating through data analysis tasks.
- Dynamic data filtering, downloading, and updating (catalog, picking, stations, sites, etc.).

---

## Snapshots of Some Features
### 1. Secure and Robust Authentication
Manage user access, signup, login, reset password, and prevent outsider from accessing the internal organization's data.
<div align='center'>
    <img src='documentation/feature_captures/loginpage.png'>
</div>

### 2. Intuitive Upload Form for Real-Time Collaboration
Quickly update data through a user-friendly form designed for seamless collaboration and manageable changes.
<div align='center'>
    <img src='documentation/feature_captures/upload_form.png'>
</div>

### 3. Dynamic spatial filter
Filter and explore data geographically with an interactive spatial filter.
<div align='center'>
    <img src='documentation/feature_captures/filter.png'>
</div>

### 4. Interactive Data Visualizations & Analytics
Gain insights through rich, interactive charts and analytics tools.
<div align='center'>
    <img src='documentation/feature_captures/interactive.png'>
</div>

### 6. Niche Earthquake Statistical Analytics
The backend data processing engine takes care of specific earthquake analytics, like the Gutenberg-Richter analysis we have here.
<div align='center'>
    <img src='documentation/feature_captures/statistical_analytics.png'>
</div>

### 6. Powerful Yet User-Friendly Django Admin Interface
For easy, less technical (SQL) database management.
<div align='center'>
    <img src='documentation/feature_captures/admin.png'>
</div>

And many more features under continuous development...

---

## Getting Started

If you'd like to test this app using **Docker** on your local machine, the following instructions will help you set it up and run it locally.

Please note that, due to data confidentiality policies, the database contents are not included, so the app will appear blank. Which means you also have to set the Admin settings and credentials manually.

If you're interested in the database structure, feel free to contact me via email at [edelo.arham@gmail.com](mailto:edelo.arham@gmail.com), the developer will provide you full dummy database.

### Prerequisites

Ensure you have the following installed:

- **Docker**: For containerization.
- **Docker Compose**: For managing multi-container Docker applications.

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/microearthquake-dashboard.git
cd microearthquake-dashboard
```

### Running the Application

1. **Setup Environment Variables**: Create a `.env` file and configure the necessary variables (check webapp/settings.py):
    ```env
    DB_URL=postgres://yourusername:yourpassword@db:5432/yourdbname
    MAPBOX_API_TOKEN=your_mapbox_token
    ```

2. **Building and Running Docker Containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Dashboard**: Open your browser and go to [http://localhost:8000](http://localhost:8000). 

---

## Project Structure

```plaintext
microearthquake-dashboard/
│
├── .github
│   └── workflows
│       └── build-push-deploy.yml
├── .gitignore
├── LICENSE
├── README.md
├── dir_tree.txt
├── django_project
│   ├── account
│   ├── db.sqlite3
│   ├── frontpage
│   ├── manage.py
│   ├── project
│   ├── static
│   │   └── js
│   │   └── media
│   └── webapp
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── docker-compose.yml
├── documentation
│   ├── demo.gif
│   └── schematic.png
├── fastapi_service
│   ├── app
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
└── infrastructure
    └── docker
        ├── django
        │   ├── .dockerignore
        │   ├── Dockerfile
        │   └── entrypoint.prod.sh
        └── nginx
            ├── Dockerfile.nginx
            └── nginx.conf
```

## Future Improvements

### Enhancements in Automatic Hypocenter Processing

Current improvements are focused on developing advanced backend data engine functionalities with FastAPI to enable:

- **Automatic Hypocenter Determination**: Implement algorithms that can automatically identify hypocenter locations from seismic data.
- **Hypocenter Relocation Methods**: Improve existing methodologies for relocating hypocenters based on improved data input and processing techniques.
- **Moment Magnitude Calculations**: Enable automatic computation of moment magnitudes for detected seismic events.
- **Post Data Analytics**: Incorporate analytical methods to gain a better understanding of microearthquake activity across all monitored sites.


These enhancements will make the application more robust for internal development, streamline workflows, and provide more accurate real-time analyses of seismic data in microearthquake monitoring.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Technology Stacks

- **Django**: For the framework, take advantage of robust, secure auth and powerful Django ORM.
- **FastAPI**: Lightning-fast backend, serve API calls for any data processing or Machine Learning service request with asynchronous capabilities.
- **PostgreSQL/PostGIS**: For database/handling geographical data.
- **AWS RDS**: Relational database cloud service for hosting PostgreSQL.
- **Plotly JS**: For rich interactive data visualizations frontend.
- **Docker**: For containerizing the application.
- **DigitalOcean Droplets**: For deployment.

For more information on project usage, please refer to the codebase or contact the project maintainers : [edelo.arham@gmail.com](mailto:edelo.arham@gmail.com).
