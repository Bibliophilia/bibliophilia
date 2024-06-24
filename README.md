# Bibliophilia
![image](https://github.com/Bibliophilia/bibliophilia/assets/69720999/a612f73e-e4e9-4bfd-abf1-c4c21e06ac7b)



#### NSU CS Software Design 2024

Team:
Vladislav Tatarintsev (Backend) 
Anna Potapova (Backend)
Rofikul Masud (Frontend)


#### Description

Bibliophilia is a user-friendly, open-source digital library application designed to provide free access to a vast collection of books, articles, and documents. It empowers users with:

**Seamless Search:** Leverage semantic search capabilities for efficient discovery of relevant content.
**Diverse Uploads and Downloads:** Upload and download books, articles, and documents in various formats for convenient access.
**Granular Access Control:** Control who can access your uploaded content. Grant access to specific users or make public requests for access.
**Review and Rating System:** Contribute valuable feedback by writing reviews and rating books to guide other users.


## Getting Started
This guide outlines the steps to set up and use Bibliophilia as a regular user.

Prerequisites:
Docker installed [Install docker in your computer ] (https://docs.docker.com/engine/install/)


1. Clone the Repository
```bash
git clone https://github.com/Bibliophilia/bibliophilia.git
```


2. Run the Application with Docker Compose
Navigate to the `bibliophilia` directory and execute the following command to start all the required services:
```bash
docker-compose up -d
```
This command will pull the necessary Docker images, create containers for each service (frontend, backend, database, search engine, and data visualization), and run them in the background.

#### Using the Web App

The web app provides a user-friendly interface for interacting with the digital library. Here are some key features:

Search: Utilize the search bar to find books, articles, or documents using keywords or semantic search.
Browse: Explore the library's collection based on categories or other browsing options (to be implemented).
Upload Content: Contribute to the library by uploading ebooks, articles, or documents in supported formats.
Download Content: Download available content for offline reading or reference.
Access Control: Manage access permissions for your uploaded content. Grant access to specific users or require access requests for others.
Review and Rating: Share your insights and help others by writing reviews and rating content.
Note: To unlock certain advanced features (e.g., upload, access control, review/rating), you might need to create an account within the Bibliophilia web app.



### Disclaimer
The availability of specific features or functionalities might be under development and subject to change.

### Contributing
Contributions to this web app are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.
