# Roboblog

Roboblog is a Jekyll-based blogging platform that integrates with GitHub webhooks to automatically update your site whenever you create a new public gist or repository. This repository includes all the files necessary to set up and run the Roboblog platform.

## Requirements

- Docker
- Docker Compose

## Getting Started

1. Clone this repository to your server.
2. Create a `.env` file in the project directory with the following contents:

    ```.env
    WEBHOOK_SECRET=my-secret
    GITHUB_TOKEN=my-github-token
    WEBHOOK_REPO_OWNER=my-github-username
    WEBHOOK_REPO_NAME=my-github-repository
    ```

    Replace the values with your own webhook secret, GitHub token, and repository owner/name.

3. Run `docker-compose up -d` to start the Jekyll and Flask containers in detached mode.
4. Once the containers are running, navigate to `http://localhost` in your browser to view the blog.

## File Structure

- `webhook/`: Contains the files necessary to run the Flask server that listens for GitHub webhook events:
  - `app.py`: Contains the Flask application code.
  - `requirements.txt`: Contains the Python dependencies required for the Flask server.
  - `Dockerfile.flask`: Contains the Dockerfile used to build the Flask container.
- `_layouts/`: Contains the Jekyll layout files used to generate the site.
- `_posts/`: Contains the Jekyll posts used to generate the site. These posts are automatically generated by the Flask server and placed in this directory.
- `_config.yml`: Contains the Jekyll configuration settings.
- `Dockerfile`: Contains the Dockerfile used to build the Jekyll container.
- `docker-compose.yml`: Contains the Docker Compose configuration used to run the Jekyll and Flask containers.
- `fetch-github-posts.sh`: Contains the shell script used to fetch GitHub posts and update the site.
- `Gemfile`: Contains the Ruby dependencies required for Jekyll.
- `index.html`: Contains the homepage HTML for the site.
- `README.md`: Contains the project documentation.

## Updating the Site

Whenever you create a new public gist or repository, the Flask server will receive a webhook event and trigger the `fetch-github-posts.sh` script. This script will fetch the latest posts from GitHub and update the Jekyll site.

## Contributing

If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request. Contributions are welcome and appreciated!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
