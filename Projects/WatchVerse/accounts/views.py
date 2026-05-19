from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import random

from .models import User, Follow, Activity, Genre, MediaItem, Review, UserProgress, Collection, Discussion
from .tmdb_utils import TMDBHelper

class DynamicMediaItem:
    """Wrapper class to emulate MediaItem model for on-the-fly TMDB results."""
    def __init__(self, tmdb_data, media_type="movie"):
        self.tmdb_id = tmdb_data.get('id')
        m_type = media_type.lower()
        # Ensure we capture 'tv' vs 'movie'
        if m_type not in ["movie", "tv", "series", "anime", "animated_movies", "animated_series", "web_series"]:
            m_type = "movie" if tmdb_data.get('title') else "tv"
            
        self.id = f"{m_type}-{self.tmdb_id}"
        self.title = tmdb_data.get('title') or tmdb_data.get('name') or tmdb_data.get('original_title') or tmdb_data.get('original_name') or "Untitled"
        self.description = tmdb_data.get('overview', '')
        self.media_type = "MOVIE" if m_type in ["movie", "animated_movies"] else "SERIES"
        
        # Detect Anime
        genre_ids = tmdb_data.get('genre_ids', [])
        genres = tmdb_data.get('genres', [])
        genre_names = [g.get('name', '').lower() for g in genres]
        if 16 in genre_ids or "animation" in genre_names:
            if tmdb_data.get('original_language') == 'ja' or "JP" in tmdb_data.get('origin_country', []):
                self.media_type = "ANIME"

        self.tmdb_poster_path = tmdb_data.get('poster_path')
        self.tmdb_backdrop_path = tmdb_data.get('backdrop_path')
        
        release_date = tmdb_data.get('release_date') or tmdb_data.get('first_air_date')
        self.release_year = int(release_date[:4]) if release_date else 2024
        self.rating_avg = round(float(tmdb_data.get('vote_average', 0.0)), 1)
        
        # Set verdict
        if self.rating_avg >= 8.0:
            self.verdict = 'PEAK'
        elif self.rating_avg >= 7.0:
            self.verdict = 'WW'
        elif self.rating_avg >= 5.0:
            self.verdict = 'OTW'
        else:
            self.verdict = 'SKIP'

    @property
    def get_poster_url(self):
        if self.tmdb_poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.tmdb_poster_path}"
        return None

    @property
    def get_backdrop_url(self):
        if self.tmdb_backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.tmdb_backdrop_path}"
        return None

def wrap_tmdb_results(results, media_type="movie"):
    """Helper to merge TMDB results with local DB items to avoid duplicate lookups."""
    if not results:
        return []
    
    tmdb_ids = [item.get('id') for item in results if item.get('id')]
    local_items = {item.tmdb_id: item for item in MediaItem.objects.filter(tmdb_id__in=tmdb_ids)}
    
    wrapped = []
    for item in results:
        t_id = item.get('id')
        if t_id in local_items:
            wrapped.append(local_items[t_id])
        else:
            wrapped.append(DynamicMediaItem(item, media_type))
    return wrapped


# --- AUTHENTICATION & PROFILE VIEWS (PRESERVED) ---

def send_otp_email(user):
    otp = user.generate_otp()
    subject = 'Your WatchVerse Verification Code'
    message = f'Hi {user.full_name},\n\nYour OTP for WatchVerse is: {otp}. It will expire in 10 minutes.\n\nHappy Watching!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(email=email, password=password, full_name=full_name)
            send_otp_email(user)
            request.session['verify_email'] = email
            return redirect('verify-otp')
            
    return render(request, 'accounts/register.html')

def verify_otp_view(request):
    email = request.session.get('verify_email')
    if not email:
        return redirect('register')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        try:
            user = User.objects.get(email=email)
            if user.otp == otp_entered and user.otp_created_at > timezone.now() - timedelta(minutes=10):
                user.is_verified = True
                user.otp = None
                user.save()
                login(request, user)
                messages.success(request, 'Email verified successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except User.DoesNotExist:
            return redirect('register')
            
    return render(request, 'accounts/verify_otp.html', {'email': email})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.is_verified:
                send_otp_email(user)
                request.session['verify_email'] = email
                return redirect('verify-otp')
            
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'accounts/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_otp_email(user)
            request.session['reset_email'] = email
            return redirect('reset-password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            
    return render(request, 'accounts/forgot_password.html')

def reset_password_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot-password')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        new_password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.otp == otp_entered and user.otp_created_at > timezone.now() - timedelta(minutes=10):
                user.set_password(new_password)
                user.otp = None
                user.save()
                messages.success(request, 'Password reset successfully. Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except User.DoesNotExist:
            return redirect('forgot-password')
            
    return render(request, 'accounts/reset_password.html', {'email': email})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request, email=None):
    if email:
        user = User.objects.get(email=email)
    else:
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
            
    profile = user.profile
    followers_count = user.followers.count()
    following_count = user.following.count()
    
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        
    tab = request.GET.get('tab', 'activity')
    
    context = {
        'target_user': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'active_tab': tab,
    }
    
    if tab == 'activity':
        context['activities'] = user.activities.all()[:20]
    elif tab == 'reviews':
        context['reviews'] = user.reviews.all()
    elif tab == 'watchlist':
        context['watchlist'] = profile.watchlist.all()
    elif tab == 'favorites':
        context['favorites'] = profile.favorites.all()
        
    return render(request, 'accounts/profile.html', context)

def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    profile = request.user.profile
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        bio = request.POST.get('bio')
        genres = request.POST.get('favorite_genres')
        avatar = request.FILES.get('avatar')
        banner = request.FILES.get('banner')
        is_public = request.POST.get('is_public') == 'on'
        
        request.user.full_name = full_name
        request.user.save()
        
        profile.bio = bio
        profile.favorite_genres = genres
        profile.is_public = is_public
        if avatar:
            profile.avatar = avatar
        if banner:
            profile.banner = banner
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
        
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

def follow_user_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    target_user = User.objects.get(id=user_id)
    follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    
    if not created:
        follow_obj.delete()
        action = 'unfollowed'
    else:
        action = 'followed'
        Activity.objects.create(user=request.user, activity_type='FOLLOW', description=f"Started following {target_user.full_name}")
        
    return redirect('profile', email=target_user.email)


# --- DYNAMIC EXPLORATION & DISCOVERY VIEWS ---

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # 1. Fetch Featured Hero Slider (Top 5 trending all-type content)
    trending_all = TMDBHelper.fetch_trending("all", "day")[:5]
    featured_items = wrap_tmdb_results(trending_all, "movie")

    # 2. Fetch Trending Grids
    trending_movies = wrap_tmdb_results(TMDBHelper.discover_content("movie", page=1).get('results', [])[:10], "movie")
    trending_series = wrap_tmdb_results(TMDBHelper.discover_content("series", page=1).get('results', [])[:10], "tv")
    trending_anime = wrap_tmdb_results(TMDBHelper.discover_content("anime", page=1).get('results', [])[:10], "tv")

    # 3. Community Peak Picks (highly rated global content)
    peak_picks = wrap_tmdb_results(TMDBHelper.discover_content("movies", page=1, sort_by="vote_average.desc").get('results', [])[:10], "movie")

    # 4. Hidden Gems (niche but highly rated content)
    hidden_gems = wrap_tmdb_results(TMDBHelper.discover_content("movies", page=1, sort_by="popularity.desc").get('results', [])[:10], "movie")

    # 5. Local Collections, Discussions, & Continue Watching (standard DB elements)
    continue_watching = UserProgress.objects.filter(user=request.user)[:5]
    latest_reviews = Review.objects.all().order_by('-created_at')[:10]
    collections = Collection.objects.filter(is_public=True).order_by('-created_at')[:6]
    discussions = Discussion.objects.all().order_by('-created_at')[:5]

    # 6. Dynamic TMDB Genre Picks
    genre_sections = []
    # Dynamic genres (Action, Comedy, Sci-Fi)
    genres_to_discover = [
        {"name": "Action Thrillers", "id": 28, "type": "movie"},
        {"name": "Sci-Fi & Fantasy", "id": 878, "type": "movie"},
        {"name": "Hilarious Comedy", "id": 35, "type": "movie"}
    ]
    for genre in genres_to_discover:
        items = wrap_tmdb_results(TMDBHelper.discover_content(genre["type"], page=1, genre_ids=genre["id"]).get('results', [])[:10], genre["type"])
        if items:
            genre_sections.append({
                'genre': {'name': genre["name"]},
                'items': items
            })

    context = {
        'featured': featured_items,
        'trending_movies': trending_movies,
        'trending_anime': trending_anime,
        'trending_series': trending_series,
        'peak_picks': peak_picks,
        'continue_watching': continue_watching,
        'latest_reviews': latest_reviews,
        'hidden_gems': hidden_gems,
        'collections': collections,
        'discussions': discussions,
        'genre_sections': genre_sections,
    }
    return render(request, 'accounts/home.html', context)


def media_detail_view(request, media_id):
    """Dynamic detail view resolving standard IDs or TMDB hybrid IDs on the fly."""
    extra_data = {
        'cast': [],
        'director': None,
        'trailer': None,
        'providers': [],
        'mood_tags': [],
        'screenshots': [],
        'similar': []
    }

    if '-' in str(media_id):
        # Format: 'movie-12345' or 'tv-67890'
        m_type, tmdb_id_str = str(media_id).split('-')
        tmdb_id = int(tmdb_id_str)
        
        # Check if already saved in DB
        media_item = MediaItem.objects.filter(tmdb_id=tmdb_id).first()
        if not media_item:
            # Sync on demand
            details = TMDBHelper.fetch_details(tmdb_id, media_type=m_type)
            if details:
                media_item = TMDBHelper.sync_to_db(details, media_type=m_type)
            else:
                messages.error(request, "Failed to load content details from TMDB.")
                return redirect('home')
    else:
        # Standard integer ID
        media_item = get_object_or_404(MediaItem, id=int(media_id))
        tmdb_id = media_item.tmdb_id

    # Fetch fresh auxiliary data directly from TMDB for maximum detail completeness
    if tmdb_id:
        m_type = "movie" if media_item.media_type == "MOVIE" else "tv"
        details = TMDBHelper.fetch_details(tmdb_id, media_type=m_type)
        
        if details:
            # Credits / Cast / Director
            credits = details.get('credits', {})
            extra_data['cast'] = credits.get('cast', [])[:10]
            
            # Find Director/Creator
            crew = credits.get('crew', [])
            directors = [member['name'] for member in crew if member.get('job') == 'Director']
            if directors:
                extra_data['director'] = ", ".join(directors)
            else:
                # Fallback for TV series
                created_by = details.get('created_by', [])
                if created_by:
                    extra_data['director'] = ", ".join([creator['name'] for creator in created_by])

            # Videos / Trailer
            videos = details.get('videos', {}).get('results', [])
            for video in videos:
                if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                    extra_data['trailer'] = f"https://www.youtube-nocookie.com/embed/{video['key']}"
                    break

            # Providers
            providers_data = details.get('watch/providers', {}).get('results', {}).get('US', {})
            extra_data['providers'] = providers_data.get('flatrate', [])[:5]

            # Screenshots / Images
            images = details.get('images', {}).get('backdrops', [])
            extra_data['screenshots'] = [img.get('file_path') for img in images[:6]]

            # Mood tags
            genres = details.get('genres', [])
            extra_data['mood_tags'] = [g.get('name') for g in genres[:3]]
            if media_item.rating_avg >= 8.0:
                extra_data['mood_tags'].append("Masterpiece")
            elif media_item.rating_avg >= 7.0:
                extra_data['mood_tags'].append("Highly Rated")

            # Similar / Recommendations
            similar_raw = details.get('similar', {}).get('results', [])[:6]
            extra_data['similar'] = wrap_tmdb_results(similar_raw, m_type)

    reviews = media_item.reviews.all().order_by('-created_at')
    context = {
        'item': media_item,
        'reviews': reviews,
        'similar_content': extra_data['similar'],
        'extra': extra_data,
        'rating_range': range(1, 11)
    }
    return render(request, 'accounts/media_detail.html', context)


def search_view(request):
    """Dynamic multi-language fuzzy search page."""
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    
    results = []
    total_pages = 1
    total_results = 0
    
    if query:
        search_data = TMDBHelper.search_multi(query, page)
        raw_results = search_data.get('results', [])
        
        # Filter down results to only movies and tv shows
        filtered_raw = []
        for res in raw_results:
            media_type = res.get('media_type')
            if media_type in ['movie', 'tv']:
                filtered_raw.append(res)
                
        # Merge with local database matches to support standard IDs where possible
        results = wrap_tmdb_results(filtered_raw)
        total_pages = search_data.get('total_pages', 1)
        total_results = search_data.get('total_results', 0)
        
    context = {
        'query': query,
        'results': results,
        'page': page,
        'total_pages': total_pages,
        'total_results': total_results,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None
    }
    return render(request, 'accounts/search.html', context)


def search_api_view(request):
    """Instant AJAX search autocomplete provider."""
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
        
    search_data = TMDBHelper.search_multi(query, 1)
    results = search_data.get('results', [])[:6]
    
    suggestions = []
    for res in results:
        media_type = res.get('media_type')
        if media_type not in ['movie', 'tv']:
            continue
            
        title = res.get('title') or res.get('name') or res.get('original_title')
        release_date = res.get('release_date') or res.get('first_air_date')
        year = release_date[:4] if release_date else ""
        poster_path = res.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w92{poster_path}" if poster_path else None
        
        suggestions.append({
            'id': f"{media_type}-{res.get('id')}",
            'title': title,
            'year': year,
            'media_type': media_type.upper(),
            'poster_url': poster_url
        })
        
    return JsonResponse({'results': suggestions})


def explore_view(request):
    """Multi-dimensional explorer interface supporting categories, countries, languages, and genres."""
    category = request.GET.get('category', 'movies').lower()
    genre_id = request.GET.get('genre', '')
    language = request.GET.get('lang', '')
    country = request.GET.get('country', '')
    page = int(request.GET.get('page', 1))
    sort_by = request.GET.get('sort', 'popularity.desc')

    # Convert request category to discover endpoint argument
    content_type = "movies"
    if category in ["series", "tv"]:
        content_type = "series"
    elif category == "anime":
        content_type = "anime"
    elif category == "documentaries":
        content_type = "documentaries"
    elif category == "animated_movies":
        content_type = "animated_movies"
    elif category == "animated_series":
        content_type = "animated_series"
    elif category == "web_series":
        content_type = "web_series"
    elif category == "ott_originals":
        content_type = "ott_originals"

    discover_data = TMDBHelper.discover_content(
        content_type=content_type,
        page=page,
        genre_ids=genre_id if genre_id else None,
        language=language if language else None,
        country=country if country else None,
        sort_by=sort_by
    )

    raw_results = discover_data.get('results', [])
    m_type = "tv" if category in ["series", "tv", "anime", "animated_series", "web_series"] else "movie"
    results = wrap_tmdb_results(raw_results, media_type=m_type)
    total_pages = discover_data.get('total_pages', 1)

    # Context filters configuration lists
    languages_list = [
        {"code": "en", "name": "English"},
        {"code": "hi", "name": "Hindi"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "ta", "name": "Tamil"},
        {"code": "te", "name": "Telugu"},
        {"code": "ml", "name": "Malayalam"}
    ]
    countries_list = [
        {"code": "US", "name": "USA"},
        {"code": "IN", "name": "India"},
        {"code": "JP", "name": "Japan"},
        {"code": "KR", "name": "Korea"},
        {"code": "CN", "name": "China"},
        {"code": "GB", "name": "United Kingdom"}
    ]
    
    context = {
        'category': category,
        'genre': genre_id,
        'lang': language,
        'country': country,
        'sort': sort_by,
        'results': results,
        'page': page,
        'total_pages': min(total_pages, 500),  # TMDB limits discover queries to page 500
        'languages': languages_list,
        'countries': countries_list,
        'next_page': page + 1 if page < min(total_pages, 500) else None,
        'prev_page': page - 1 if page > 1 else None
    }
    return render(request, 'accounts/category.html', context)
