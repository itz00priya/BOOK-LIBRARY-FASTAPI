document.addEventListener('DOMContentLoaded', () => {
    // Auth Check
    const token = localStorage.getItem('token');
    if (!token && !window.location.pathname.includes('login') && !window.location.pathname.includes('register')) {
        window.location.href = '/login';
        return;
    }

    // State
    let books = [];
    let stats = {
        totalBooks: 0,
        availableBooks: 0,
        activeBorrowings: 0,
        overdue: 0
    };

    // DOM Elements
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');
    const recentBooksList = document.getElementById('recent-books-list');
    const allBooksList = document.getElementById('all-books-list');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const userEmailEl = document.getElementById('user-email');
    const userInitialsEl = document.getElementById('user-initials');

    // Update User Info
    if (localStorage.getItem('user_email')) {
        const email = localStorage.getItem('user_email');
        if (userEmailEl) userEmailEl.innerText = email;
        if (userInitialsEl) userInitialsEl.innerText = email.substring(0, 2).toUpperCase();
    }

    // Logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.clear();
            window.location.href = '/login';
        });
    }

    // Navigation
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetView = item.getAttribute('data-view');

            // Update active nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update visible view
            views.forEach(view => {
                if (view.id === `${targetView}-view`) {
                    view.classList.add('active');
                } else {
                    view.classList.remove('active');
                }
            });

            if (targetView === 'books') {
                fetchAllBooks();
            }
        });
    });

    // View All links
    document.querySelectorAll('.view-all').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('data-target');
            document.querySelector(`.nav-item[data-view="${target}"]`).click();
        });
    });

    // Fetch Data
    async function fetchDashboardStats() {
        try {
            // In a real app, these would be specific aggregate endpoints.
            // For now, we'll fetch books and borrowings to calculate.
            const booksResponse = await fetch('/api/v1/books/?limit=100');
            const borrowingsResponse = await fetch('/api/v1/borrowing/?status=BORROWED');

            if (booksResponse.ok) {
                const booksData = await booksResponse.json();
                stats.totalBooks = booksData.length;
                stats.availableBooks = booksData.reduce((acc, book) => acc + (book.available_copies > 0 ? 1 : 0), 0);
            }

            if (borrowingsResponse.ok) {
                const borrowingsData = await borrowingsResponse.json();
                stats.activeBorrowings = borrowingsData.length;
            }

            updateStatsUI();
            if (stats.totalBooks > 0) {
                const booksResponse = await fetch('/api/v1/books/?limit=5');
                const booksData = await booksResponse.json();
                renderRecentBooks(booksData);
            }
        } catch (error) {
            console.error('Error fetching stats:', error);
        }
    }

    async function fetchAllBooks(search = '') {
        try {
            let url = '/api/v1/books/?limit=50';
            if (search) url += `&search=${encodeURIComponent(search)}`;

            const response = await fetch(url);
            if (response.ok) {
                const data = await response.json();
                renderAllBooks(data);
            }
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    }

    // UI Rendering
    function updateStatsUI() {
        statTotalBooks.innerText = stats.totalBooks;
        statAvailableBooks.innerText = stats.availableBooks;
        statActiveBorrowings.innerText = stats.activeBorrowings;
        statOverdue.innerText = stats.overdue;
    }

    function renderRecentBooks(books) {
        recentBooksList.innerHTML = books.map(book => `
            <tr>
                <td><strong>${book.title}</strong></td>
                <td>${book.author}</td>
                <td><span class="badge badge-success">${book.genre}</span></td>
                <td>${book.available_copies > 0 ? '✅ Available' : '❌ Out of Stock'}</td>
            </tr>
        `).join('');
    }

    function renderAllBooks(books) {
        allBooksList.innerHTML = books.map(book => `
            <tr>
                <td>#${book.id}</td>
                <td><strong>${book.title}</strong></td>
                <td>${book.author}</td>
                <td>${book.genre}</td>
                <td>${book.available_copies} / ${book.total_copies}</td>
                <td>
                    <button class="btn btn-sm" onclick="alert('Edit book ${book.id}')">✏️</button>
                    <button class="btn btn-sm" onclick="alert('Delete book ${book.id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
    }

    // Search
    searchBtn.addEventListener('click', () => {
        const query = searchInput.value;
        const activeNav = document.querySelector('.nav-item.active').getAttribute('data-view');

        if (activeNav === 'dashboard') {
            document.querySelector('.nav-item[data-view="books"]').click();
        }
        fetchAllBooks(query);
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBtn.click();
    });

    // Initial Load
    fetchDashboardStats();
});
