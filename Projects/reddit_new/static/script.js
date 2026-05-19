document.addEventListener('DOMContentLoaded', () => {
    
    // --- Theme Toggle ---
    const themeBtn = document.querySelector('.theme-toggle');
    const htmlElement = document.documentElement;
    const themeIcon = themeBtn.querySelector('i');

    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.replace('ph-moon', 'ph-sun');
        } else {
            themeIcon.classList.replace('ph-sun', 'ph-moon');
        }
    }

    // Default theme based on HTML attribute
    updateThemeIcon(htmlElement.getAttribute('data-theme'));

    themeBtn.addEventListener('click', () => {
        let currentTheme = htmlElement.getAttribute('data-theme');
        let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // --- Sidebar Toggle ---
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.getElementById('sidebar');

    menuToggle.addEventListener('click', () => {
        // For desktop layout (margin logic in CSS)
        sidebar.classList.toggle('closed');
        // For mobile layout (offcanvas logic)
        sidebar.classList.toggle('open');
    });

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // --- Formatting Numbers ---
    function parseVoteCount(str) {
        if (str.includes('k')) {
            return parseFloat(str.replace('k', '')) * 1000;
        } else if (str.includes('m')) {
            return parseFloat(str.replace('m', '')) * 1000000;
        }
        return parseInt(str.replace(/,/g, ''));
    }

    function formatVoteCount(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'm';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'k';
        }
        // Add commas
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // --- Vote Functionality ---
    const voteWidgets = document.querySelectorAll('.vote-widget');

    voteWidgets.forEach(widget => {
        const upBtn = widget.querySelector('.upvote');
        const downBtn = widget.querySelector('.downvote');
        const countSpan = widget.querySelector('.vote-count');
        
        let originalCount = parseVoteCount(countSpan.textContent);
        let currentVote = 0; // 0 = none, 1 = up, -1 = down

        upBtn.addEventListener('click', () => {
            if (currentVote === 1) {
                // Remove upvote
                currentVote = 0;
                upBtn.classList.remove('upvoted');
            } else {
                // Add upvote
                currentVote = 1;
                upBtn.classList.add('upvoted');
                downBtn.classList.remove('downvoted');
            }
            updateVoteDisplay();
        });

        downBtn.addEventListener('click', () => {
            if (currentVote === -1) {
                // Remove downvote
                currentVote = 0;
                downBtn.classList.remove('downvoted');
            } else {
                // Add downvote
                currentVote = -1;
                downBtn.classList.add('downvoted');
                upBtn.classList.remove('upvoted');
            }
            updateVoteDisplay();
        });

        function updateVoteDisplay() {
            let newCount = originalCount + currentVote;
            countSpan.textContent = formatVoteCount(newCount);
            
            // Adjust color of the count number
            countSpan.classList.remove('up', 'down');
            if (currentVote === 1) countSpan.classList.add('up');
            if (currentVote === -1) countSpan.classList.add('down');
        }
    });

    // --- Join Buttons ---
    const joinBtns = document.querySelectorAll('.join-btn');
    
    joinBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.classList.contains('joined')) {
                this.classList.remove('joined');
                this.textContent = 'Join';
            } else {
                this.classList.add('joined');
                this.textContent = 'Joined';
            }
        });
    });

    // --- Sorting Interaction ---
    const sortBtns = document.querySelectorAll('.feed-sort .sort-btn');
    
    // Ignore the last button which is a layout toggle icon
    for(let i = 0; i < sortBtns.length - 1; i++) {
        sortBtns[i].addEventListener('click', (e) => {
            document.querySelector('.sort-btn.active').classList.remove('active');
            e.target.classList.add('active');
        });
    }

});
