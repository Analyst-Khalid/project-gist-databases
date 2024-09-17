import requests
import sqlite3

def import_gists_to_database(db, username, commit=True):
    url = 'https://api.github.com/users/{user}/gists'.format(user=username)
    response = requests.get(url)
    response = response.json()
    cur = db.cursor()

    for gist in response:
        par = {
            'github_id': gist['id'], 
            'html_url': gist.get('html_url', ''), 
            'git_pull_url': gist.get('git_pull_url', ''), 
            'git_push_url': gist.get('git_push_url', ''), 
            'commits_url': gist.get('commits_url', ''), 
            'forks_url': gist.get('forks_url', ''), 
            'public': gist.get('public', False), 
            'created_at': gist['created_at'], 
            'updated_at': gist['updated_at'], 
            'comments': gist.get('comments', 0), 
            'comments_url': gist.get('comments_url', '')
        }

        query = """
        INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, commits_url, 
        forks_url, public, created_at, updated_at, comments, comments_url)
        VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url, 
        :forks_url, :public, :created_at, :updated_at, :comments, :comments_url);
        """
        cur.execute(query, par)

    if commit:
        db.commit()


