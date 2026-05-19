// ==============================
// 🌙 DARK / LIGHT MODE
// ==============================
const themeBtn = document.getElementById("themeToggle");

if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        // toggle icon
        if (document.body.classList.contains("dark-mode")) {
            themeBtn.classList.remove("bi-moon");
            themeBtn.classList.add("bi-sun");
            localStorage.setItem("theme", "dark");
        } else {
            themeBtn.classList.remove("bi-sun");
            themeBtn.classList.add("bi-moon");
            localStorage.setItem("theme", "light");
        }
    });
}

// Load saved theme
window.addEventListener("load", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        if (themeBtn) {
            themeBtn.classList.remove("bi-moon");
            themeBtn.classList.add("bi-sun");
        }
    } else if (savedTheme === "light") {
        document.body.classList.remove("dark-mode");
        if (themeBtn) {
            themeBtn.classList.remove("bi-sun");
            themeBtn.classList.add("bi-moon");
        }
    }
});


// ==============================
// 🔄 LOAD MORE BUTTON
// ==============================
document.addEventListener("DOMContentLoaded", function () {

    const loadMoreBtn = document.getElementById("loadMoreBtn");
    const container = document.getElementById("posts-container");

    console.log(loadMoreBtn, container); // 🔍 DEBUG

    if (!loadMoreBtn || !container) return;

    loadMoreBtn.addEventListener("click", () => {

        for (let i = 0; i < 2; i++) {

            const newItem = document.createElement("div");
            newItem.className = "blog-item d-flex mb-4";

            newItem.innerHTML = `
                <div class="flex-grow-1 me-3">
                    <span class="badge bg-danger mb-2">NEW</span>
                    <h4>New Loaded Article Title</h4>
                    <p>This is dynamically loaded content like Wesper.</p>
                    <small>BY ADMIN • JUST NOW</small>
                </div>

                <div class="blog-img">
                    <img src="https://picsum.photos/300/200?random=${Math.random()}">
                </div>
            `;

            container.appendChild(newItem);
        }

    });

});


// ==============================
// 🧭 SMOOTH SCROLL (TRENDING)
// ==============================
const trending = document.querySelector(".trending-scroll");

let isDown = false;
let startX;
let scrollLeft;

if (trending) {
    trending.addEventListener("mousedown", (e) => {
        isDown = true;
        startX = e.pageX - trending.offsetLeft;
        scrollLeft = trending.scrollLeft;
    });

    trending.addEventListener("mouseleave", () => {
        isDown = false;
    });

    trending.addEventListener("mouseup", () => {
        isDown = false;
    });

    trending.addEventListener("mousemove", (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - trending.offsetLeft;
        const walk = (x - startX) * 2;
        trending.scrollLeft = scrollLeft - walk;
    });
}


// ==============================
// 🔍 SEARCH ICON LOGIC (SIDEBAR)
// ==============================
const sidebarSearchBtn = document.getElementById("sidebarSearchBtn");
const sidebarDefaultHeader = document.getElementById("sidebarDefaultHeader");
const sidebarSearchState = document.getElementById("sidebarSearchState");
const sidebarSearchInput = document.getElementById("sidebarSearchInput");
const clearSearchBtn = document.getElementById("clearSearchBtn");
const closeSidebarInner = document.getElementById("closeSidebarInner");

if (sidebarSearchBtn) {
    sidebarSearchBtn.addEventListener("click", () => {
        if(sidebarDefaultHeader) sidebarDefaultHeader.classList.replace("d-flex", "d-none");
        if(sidebarSearchState) {
            sidebarSearchState.classList.replace("d-none", "d-flex");
            sidebarSearchInput.focus();
        }
    });
}

if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", () => {
        if(sidebarSearchInput) {
            sidebarSearchInput.value = "";
            sidebarSearchInput.focus();
        }
    });
}

// ==============================
// 🛒 BAG CLICK
// ==============================
const bagIcon = document.querySelector(".bi-bag");

bagIcon?.addEventListener("click", () => {
    alert("Cart is empty 🛒");
});


// ==============================



// ==============================
// 🎯 HOVER ANIMATION (CARDS)
// ==============================
document.querySelectorAll(".hero-card, .explore-card, .game-card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "scale(1.02)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "scale(1)";
    });
});


// ==============================
// ⬆️ SCROLL TO TOP BUTTON
// ==============================
const scrollBtn = document.createElement("div");
scrollBtn.id = "scrollToTopBtn";
scrollBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
scrollBtn.style.position = "fixed";
scrollBtn.style.bottom = "30px";
scrollBtn.style.right = "30px";
scrollBtn.style.width = "45px";
scrollBtn.style.height = "45px";
scrollBtn.style.background = "#e63946"; // Matches the main brand red
scrollBtn.style.color = "white";
scrollBtn.style.borderRadius = "50%";
scrollBtn.style.display = "none";
scrollBtn.style.alignItems = "center";
scrollBtn.style.justifyContent = "center";
scrollBtn.style.fontSize = "20px";
scrollBtn.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";
scrollBtn.style.cursor = "pointer";
scrollBtn.style.transition = "all 0.3s ease";
scrollBtn.style.zIndex = "999";

// Hover effect
scrollBtn.addEventListener("mouseenter", () => {
    scrollBtn.style.transform = "translateY(-3px)";
    scrollBtn.style.background = "#ff4d4d";
    scrollBtn.style.boxShadow = "0 6px 15px rgba(0,0,0,0.3)";
});
scrollBtn.addEventListener("mouseleave", () => {
    scrollBtn.style.transform = "translateY(0)";
    scrollBtn.style.background = "#e63946";
    scrollBtn.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";
});

document.body.appendChild(scrollBtn);

window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        scrollBtn.style.display = "flex";
    } else {
        scrollBtn.style.display = "none";
    }
});

scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

const social = document.getElementById("socialBar");
const review = document.getElementById("reviewSection");

window.addEventListener("scroll", () => {
    if (review && social) {
        if (window.innerWidth >= 992) {
            const reviewRect = review.getBoundingClientRect();
            const defaultTop = 100;
            const threshold = defaultTop + social.offsetHeight + 20;

            if (reviewRect.top < threshold) {
                const pushUp = threshold - reviewRect.top;
                social.style.top = (defaultTop - pushUp) + "px";
            } else {
                social.style.top = defaultTop + "px";
            }
        } else {
            social.style.top = "";
        }
    }
});

// ==============================
// 📱 CUSTOM SIDEBAR ACCORDION & TOGGLE 
// ==============================
const mobileMenuIcon = document.querySelector(".bi-list");
const customSidebar = document.getElementById("customSidebar");
const closeSidebarBtn = document.getElementById("closeSidebar");
const sidebarOverlay = document.getElementById("sidebarOverlay");

if (mobileMenuIcon && customSidebar) {
    mobileMenuIcon.addEventListener("click", () => {
        customSidebar.classList.add("open");
        if(sidebarOverlay) sidebarOverlay.classList.add("show");
    });
}

// Function to close sidebar cleanly
function closeCustomSidebar() {
    if(customSidebar) customSidebar.classList.remove("open");
    if(sidebarOverlay) sidebarOverlay.classList.remove("show");
    
    // Also reset the search state
    if(sidebarSearchState && sidebarSearchState.classList.contains("d-flex")) {
        sidebarSearchState.classList.replace("d-flex", "d-none");
    }
    if(sidebarDefaultHeader && sidebarDefaultHeader.classList.contains("d-none")) {
        sidebarDefaultHeader.classList.replace("d-none", "d-flex");
    }
    if(sidebarSearchInput) {
        sidebarSearchInput.value = "";
    }
}

// Mobile Icon Click Event
mobileMenuIcon?.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
});

// Close icon inside sidebar
closeSidebarBtn?.addEventListener("click", closeCustomSidebar);

// Close inner icon (in search bar)
closeSidebarInner?.addEventListener("click", closeCustomSidebar);

// Overlay click
sidebarOverlay?.addEventListener("click", closeCustomSidebar);

const sidebarCatItems = document.querySelectorAll(".sidebar-cat-item");
sidebarCatItems.forEach(item => {
    const toggleBtn = item.querySelector(".toggle-sub");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", (e) => {
            item.classList.toggle("open");
            if (item.classList.contains("open")) {
                toggleBtn.classList.remove("bi-plus");
                toggleBtn.classList.add("bi-x");
            } else {
                toggleBtn.classList.remove("bi-x");
                toggleBtn.classList.add("bi-plus");
            }
        });
    }
});

// ==============================
// 📋 FEED FILTERING LOGIC
// ==============================
document.addEventListener("DOMContentLoaded", () => {
    const filterTabs = document.querySelectorAll(".feed-filter-tabs .nav-link");
    const blogItems = document.querySelectorAll("#posts-container .blog-item");

    if (filterTabs.length > 0 && blogItems.length > 0) {
        filterTabs.forEach(tab => {
            tab.addEventListener("click", (e) => {
                e.preventDefault();
                
                // Remove active class from all tabs
                filterTabs.forEach(t => t.classList.remove("active"));
                // Add active class to clicked tab
                tab.classList.add("active");
                
                const filter = tab.getAttribute("data-filter").toUpperCase();
                
                // Filter the cards
                blogItems.forEach(item => {
                    if (filter === "ALL") {
                        item.classList.remove("d-none");
                        item.classList.add("d-flex");
                    } else {
                        // Check badge text within this specific blog item
                        const badge = item.querySelector(".badge");
                        const category = badge ? badge.textContent.trim().toUpperCase() : "";
                        
                        // If the badge matches the selected tab filter
                        if (category.includes(filter) || filter.includes(category)) {
                            item.classList.remove("d-none");
                            item.classList.add("d-flex");
                        } else {
                            item.classList.remove("d-flex");
                            item.classList.add("d-none");
                        }
                    }
                });
            });
        });
    }
});