import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def index(request):
    return render(request, 'github_app/index.html')

def list_repositories(request):
    repos = []
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            url = f'https://api.github.com/users/{username}/repos'
            response = requests.get(url)
            if response.status_code == 200:
                repos = response.json()
            else:
                messages.error(request, f"Error fetching repositories for {username}. Make sure the username is correct.")
        else:
            messages.error(request, "Please enter a username.")
            
    return render(request, 'github_app/list_repos.html', {'repos': repos})

def github_login(request):
    client_id = settings.GITHUB_CLIENT_ID
    # Requesting 'repo' scope to create repositories
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=repo"
    return redirect(url)

def github_callback(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, "GitHub authorization failed. No code received.")
        return redirect('index')

    token_url = "https://github.com/login/oauth/access_token"
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.post(token_url, data=data, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        if access_token:
            request.session['github_token'] = access_token
            messages.success(request, "Successfully logged in with GitHub!")
            return redirect('create_repository')
        else:
            messages.error(request, "Failed to obtain access token from GitHub.")
    else:
        messages.error(request, "Error communicating with GitHub OAuth API.")
        
    return redirect('index')

def github_logout(request):
    if 'github_token' in request.session:
        del request.session['github_token']
        messages.success(request, "Logged out successfully.")
    return redirect('index')

def create_repository(request):
    # Check if user is logged in via OAuth
    github_token = request.session.get('github_token')
    
    if request.method == 'POST':
        if not github_token:
            messages.error(request, "You must be logged in to create a repository.")
            return redirect('create_repository')
            
        repo_name = request.POST.get('repo_name')
        description = request.POST.get('description', '')
        private = request.POST.get('private') == 'on'
        
        if repo_name:
            url = 'https://api.github.com/user/repos'
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            data = {
                'name': repo_name,
                'description': description,
                'private': private
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                repo_data = response.json()
                messages.success(request, f"Repository '{repo_name}' created successfully! URL: {repo_data.get('html_url')}")
                return redirect('create_repository')
            else:
                messages.error(request, f"Failed to create repository. Status: {response.status_code}, Message: {response.json().get('message')}")
        else:
            messages.error(request, "Repository Name is required.")
            
    return render(request, 'github_app/create_repo.html', {'github_token': github_token})
