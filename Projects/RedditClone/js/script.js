// ----- Sample initial posts data -----
let posts = [
    {
        id: 'p1',
        subreddit: 'r/aww',
        title: 'My dog learned a new trick today!',
        content: 'He can now roll over and play dead on command. So proud of him!',
        votes: 142,
        comments: 24,
        timestamp: Date.now() - 3600000 * 5
    },
    {
        id: 'p2',
        subreddit: 'r/programming',
        title: 'Why I love vanilla JavaScript',
        content: 'No frameworks, no dependencies, just pure JS for the win.',
        votes: 89,
        comments: 15,
        timestamp: Date.now() - 3600000 * 12
    },
    {
        id: 'p3',
        subreddit: 'r/memes',
        title: 'When you finally understand the joke',
        content: 'https://i.imgur.com/placeholder.jpg',
        votes: 256,
        comments: 42,
        timestamp: Date.now() - 3600000 * 2
    }
];

// Helper to format relative time
function timeAgo(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return interval + ' years ago';
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return interval + ' months ago';
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return interval + ' days ago';
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return interval + ' hours ago';
    interval = Math.floor(seconds / 60);
    if (interval > 1) return interval + ' minutes ago';
    return 'just now';
}

// Helper to escape HTML to prevent XSS
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, function(c) {
        return c;
    });
}

// Render all posts into the DOM
function renderPosts() {
    const container = document.getElementById('postsContainer');
    if (!container) return;
    
    if (posts.length === 0) {
        container.innerHTML = '<div style="background:white; border-radius:8px; padding:32px; text-align:center; color:#7C7C7C;">No posts yet. Be the first to create one!</div>';
        return;
    }
    
    // Sort by votes descending (hot)
    const sorted = [...posts].sort((a,b) => b.votes - a.votes);
    
    let html = '';
    sorted.forEach(post => {
        html += `
            <div class="post-card" data-id="${post.id}">
                <div class="post-header">
                    <span class="subreddit">${escapeHtml(post.subreddit)}</span>
                    <span>• Posted by u/anon ${timeAgo(post.timestamp)}</span>
                </div>
                <div class="post-title">${escapeHtml(post.title)}</div>
                <div class="post-content">${escapeHtml(post.content)}</div>
                <div class="post-actions">
                    <div class="vote-group">
                        <button class="vote-btn upvote" data-id="${post.id}">▲</button>
                        <span class="vote-count" data-id="${post.id}">${post.votes}</span>
                        <button class="vote-btn downvote" data-id="${post.id}">▼</button>
                    </div>
                    <div class="comment-icon">
                        💬 <span>${post.comments} comments</span>
                    </div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
    
    // Reattach event listeners after rendering
    attachVoteEvents();
}

// Attach upvote/downvote event listeners
function attachVoteEvents() {
    document.querySelectorAll('.upvote').forEach(btn => {
        btn.removeEventListener('click', handleUpvote);
        btn.addEventListener('click', handleUpvote);
    });
    document.querySelectorAll('.downvote').forEach(btn => {
        btn.removeEventListener('click', handleDownvote);
        btn.addEventListener('click', handleDownvote);
    });
}

function handleUpvote(e) {
    const postId = e.currentTarget.getAttribute('data-id');
    const post = posts.find(p => p.id === postId);
    if (post) {
        post.votes += 1;
        renderPosts();
    }
}

function handleDownvote(e) {
    const postId = e.currentTarget.getAttribute('data-id');
    const post = posts.find(p => p.id === postId);
    if (post) {
        post.votes -= 1;
        renderPosts();
    }
}

// Add a new post
function addNewPost(title, content) {
    if (!title.trim()) {
        alert('Please enter a title');
        return false;
    }
    
    const newPost = {
        id: 'p' + Date.now(),
        subreddit: 'r/AskReddit',
        title: title.trim(),
        content: content.trim() || '(no text)',
        votes: 0,
        comments: 0,
        timestamp: Date.now()
    };
    
    posts.unshift(newPost);
    renderPosts();
    return true;
}

// Simple search filter (client-side)
function filterPostsBySearch(query) {
    if (!query.trim()) {
        renderPosts();
        return;
    }
    const lowerQuery = query.toLowerCase();
    const filtered = posts.filter(post => 
        post.title.toLowerCase().includes(lowerQuery) || 
        post.content.toLowerCase().includes(lowerQuery) ||
        post.subreddit.toLowerCase().includes(lowerQuery)
    );
    
    const container = document.getElementById('postsContainer');
    if (filtered.length === 0) {
        container.innerHTML = '<div style="background:white; border-radius:8px; padding:32px; text-align:center; color:#7C7C7C;">No matching posts found.</div>';
        return;
    }
    
    // Render filtered list
    let html = '';
    filtered.forEach(post => {
        html += `
            <div class="post-card" data-id="${post.id}">
                <div class="post-header">
                    <span class="subreddit">${escapeHtml(post.subreddit)}</span>
                    <span>• Posted by u/anon ${timeAgo(post.timestamp)}</span>
                </div>
                <div class="post-title">${escapeHtml(post.title)}</div>
                <div class="post-content">${escapeHtml(post.content)}</div>
                <div class="post-actions">
                    <div class="vote-group">
                        <button class="vote-btn upvote" data-id="${post.id}">▲</button>
                        <span class="vote-count" data-id="${post.id}">${post.votes}</span>
                        <button class="vote-btn downvote" data-id="${post.id}">▼</button>
                    </div>
                    <div class="comment-icon">💬 ${post.comments} comments</div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
    attachVoteEvents();
}

// Event listeners for new post and search
document.getElementById('submitPostBtn')?.addEventListener('click', () => {
    const title = document.getElementById('postTitle').value;
    const text = document.getElementById('postText').value;
    if (addNewPost(title, text)) {
        document.getElementById('postTitle').value = '';
        document.getElementById('postText').value = '';
    }
});

document.getElementById('searchInput')?.addEventListener('input', (e) => {
    filterPostsBySearch(e.target.value);
});

// Initial render
renderPosts();