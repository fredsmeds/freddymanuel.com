// SMART VIDEO LOADING - Only load videos when navigating to a page
        const loadedPages = new Set();
        
        function loadVideosForPage(pageName) {
            if (loadedPages.has(pageName)) {
                // If page already loaded, just play the videos
                playVideosForPage(pageName);
                return;
            }
            
            const pageElement = document.getElementById('page-' + pageName);
            if (!pageElement) return;
            
            const videos = pageElement.querySelectorAll('video');
            videos.forEach(video => {
                const sources = video.querySelectorAll('source[data-src]');
                if (sources.length > 0) {
                    sources.forEach(source => {
                        source.src = source.dataset.src;
                        source.removeAttribute('data-src');
                    });
                    video.load();
                    if (video.hasAttribute('autoplay')) {
                        video.play().catch(err => console.log("Autoplay prevented:", err));
                    }
                }
            });
            loadedPages.add(pageName);
        }

        // Pause all videos on a specific page
        function pauseVideosForPage(pageName) {
            const pageElement = document.getElementById('page-' + pageName);
            if (!pageElement) return;
            
            const videos = pageElement.querySelectorAll('video');
            videos.forEach(video => {
                if (!video.paused) {
                    video.pause();
                }
            });
        }

        // Play all videos on a specific page
        function playVideosForPage(pageName) {
            const pageElement = document.getElementById('page-' + pageName);
            if (!pageElement) return;
            
            const videos = pageElement.querySelectorAll('video');
            videos.forEach(video => {
                if (video.hasAttribute('autoplay')) {
                    video.play().catch(err => console.log("Autoplay prevented:", err));
                }
            });
        }

        // Image/Video protection
        document.addEventListener('contextmenu', function(e) {
            if (e.target.tagName === 'IMG' || e.target.tagName === 'VIDEO') {
                e.preventDefault();
            }
        });
        
        document.addEventListener('dragstart', function(e) {
            if (e.target.tagName === 'IMG' || e.target.tagName === 'VIDEO') {
                e.preventDefault();
            }
        });

document.addEventListener('DOMContentLoaded', function() {
            const carousel = document.querySelector('.page-carousel');
            const toggle = document.getElementById('menuToggle');
            const menu = document.getElementById('mobileMenu');
            const header = document.querySelector('.sticky-header');
            let timeout;
            let headerTimeout;
            let currentPage = 'about';
            let currentScrollPosition = 0;


            // PAGE NAVIGATION FUNCTION
            function navigateToPage(pageName) {
                // Pause videos from the current page before navigating
                const previousPage = currentPage;
                if (previousPage && previousPage !== pageName) {
                    pauseVideosForPage(previousPage);
                }
                
                currentPage = pageName;
                carousel.setAttribute('data-page', pageName);
                loadVideosForPage(pageName);
                
                // Update active nav items
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('data-page') === pageName) {
                        item.classList.add('active');
                    }
                });

                // Update mobile menu active items
                document.querySelectorAll('.mobile-nav-item.main-page').forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('data-page') === pageName) {
                        item.classList.add('active');
                    }
                });

                // Update URL hash
                window.location.hash = pageName;

                // Close mobile menu if open
                if (toggle && menu) {
                    toggle.classList.remove('active');
                    menu.classList.remove('active');
                }

                // Force show header immediately on page navigation (desktop only)
                if (header && window.innerWidth > 768) {
                    header.classList.add('scrolled');
                    // Hide after inactivity
                    hideHeaderAfterInactivity();
                }

                // Update header visibility based on new page scroll position
                setTimeout(checkHeaderOnPageSwitch, 100);
            }

            // SECTION NAVIGATION WITHIN ABOUT PAGE
            function navigateToSection(sectionId) {
                // First, make sure we're on the about page
                if (currentPage !== 'about') {
                    navigateToPage('about');
                    
                    // Wait for slide transition to complete
                    setTimeout(() => {
                        scrollToSection(sectionId);
                    }, 800);
                } else {
                    scrollToSection(sectionId);
                }
            }

            function scrollToSection(sectionId) {
                const aboutPage = document.getElementById('page-about');
                const targetSection = document.getElementById(sectionId);
                
                if (targetSection && aboutPage) {
                    const offset = targetSection.offsetTop;
                    aboutPage.scrollTo({
                        top: offset,
                        behavior: 'smooth'
                    });
                }

                // Close mobile menu
                if (toggle && menu) {
                    toggle.classList.remove('active');
                    menu.classList.remove('active');
                }
            }

            // DESKTOP NAV CLICKS - Main pages
            document.querySelectorAll('.nav-item[data-page]').forEach(item => {
                item.addEventListener('click', function() {
                    const page = this.getAttribute('data-page');
                    navigateToPage(page);
                });
            });

            // DESKTOP NAV CLICKS - About subsections
            document.querySelectorAll('.submenu-item[data-section]').forEach(item => {
                item.addEventListener('click', function() {
                    const section = this.getAttribute('data-section');
                    navigateToSection(section);
                });
            });

            // ONGOING SECTION NAVIGATION
            function navigateToOngoingSection(sectionId) {
                // First, make sure we're on the ongoing page
                if (currentPage !== 'ongoing') {
                    navigateToPage('ongoing');
                    
                    // Wait for slide transition to complete
                    setTimeout(() => {
                        scrollToOngoingSection(sectionId);
                    }, 800);
                } else {
                    scrollToOngoingSection(sectionId);
                }
            }

            function scrollToOngoingSection(sectionId) {
                const ongoingPage = document.getElementById('page-ongoing');
                const targetSection = document.getElementById(sectionId);
                
                if (targetSection && ongoingPage) {
                    const offset = targetSection.offsetTop;
                    ongoingPage.scrollTo({
                        top: offset,
                        behavior: 'smooth'
                    });
                }

                // Close mobile menu
                if (toggle && menu) {
                    toggle.classList.remove('active');
                    menu.classList.remove('active');
                }
            }

            // DESKTOP NAV CLICKS - Ongoing subsections
            document.querySelectorAll('.submenu-item[data-ongoing-section]').forEach(item => {
                item.addEventListener('click', function() {
                    const section = this.getAttribute('data-ongoing-section');
                    navigateToOngoingSection(section);
                });
            });

            // ARTWORK SECTION NAVIGATION
            function navigateToArtworkSection(sectionId) {
                // First, make sure we're on the artwork page
                if (currentPage !== 'artwork') {
                    navigateToPage('artwork');
                    
                    // Wait for slide transition to complete
                    setTimeout(() => {
                        scrollToArtworkSection(sectionId);
                    }, 800);
                } else {
                    scrollToArtworkSection(sectionId);
                }
            }

            function scrollToArtworkSection(sectionId) {
                const artworkPage = document.getElementById('page-artwork');
                const targetSection = document.getElementById(sectionId);
                
                if (targetSection && artworkPage) {
                    const offset = targetSection.offsetTop;
                    artworkPage.scrollTo({
                        top: offset,
                        behavior: 'smooth'
                    });
                }

                // Close mobile menu
                if (toggle && menu) {
                    toggle.classList.remove('active');
                    menu.classList.remove('active');
                }
            }

            // DESKTOP NAV CLICKS - Artwork subsections
            document.querySelectorAll('.submenu-item[data-artwork-section]').forEach(item => {
                item.addEventListener('click', function() {
                    const section = this.getAttribute('data-artwork-section');
                    navigateToArtworkSection(section);
                });
            });

            // TECH SECTION NAVIGATION
            function navigateToTechSection(sectionId) {
                // First, make sure we're on the tech page
                if (currentPage !== 'tech') {
                    navigateToPage('tech');
                    
                    // Wait for slide transition to complete
                    setTimeout(() => {
                        scrollToTechSection(sectionId);
                    }, 800);
                } else {
                    scrollToTechSection(sectionId);
                }
            }

            function scrollToTechSection(sectionId) {
                const techPage = document.getElementById('page-tech');
                const targetSection = document.getElementById(sectionId);
                
                if (targetSection && techPage) {
                    const offset = targetSection.offsetTop;
                    techPage.scrollTo({
                        top: offset,
                        behavior: 'smooth'
                    });
                }

                // Close mobile menu
                if (toggle && menu) {
                    toggle.classList.remove('active');
                    menu.classList.remove('active');
                }
            }

            // DESKTOP NAV CLICKS - Tech subsections
            document.querySelectorAll('.submenu-item[data-tech-section]').forEach(item => {
                item.addEventListener('click', function() {
                    const section = this.getAttribute('data-tech-section');
                    navigateToTechSection(section);
                });
            });

            // MOBILE MENU TOGGLE
            if (toggle && menu) {
                toggle.addEventListener('click', function() {
                    toggle.classList.toggle('active');
                    menu.classList.toggle('active');
                });

                // Mobile menu - main pages
                document.querySelectorAll('.mobile-nav-item.main-page[data-page]').forEach(item => {
                    item.addEventListener('click', function() {
                        const page = this.getAttribute('data-page');
                        navigateToPage(page);
                    });
                });

                // Mobile menu - about subsections
                document.querySelectorAll('.mobile-nav-item.subsection[data-section]').forEach(item => {
                    item.addEventListener('click', function() {
                        const section = this.getAttribute('data-section');
                        navigateToSection(section);
                    });
                });

                // Mobile menu - ongoing subsections
                document.querySelectorAll('.mobile-nav-item.subsection[data-ongoing-section]').forEach(item => {
                    item.addEventListener('click', function() {
                        const section = this.getAttribute('data-ongoing-section');
                        navigateToOngoingSection(section);
                    });
                });

                // Mobile menu - artwork subsections
                document.querySelectorAll('.mobile-nav-item.subsection[data-artwork-section]').forEach(item => {
                    item.addEventListener('click', function() {
                        const section = this.getAttribute('data-artwork-section');
                        navigateToArtworkSection(section);
                    });
                });

                // Mobile menu - tech subsections
                document.querySelectorAll('.mobile-nav-item.subsection[data-tech-section]').forEach(item => {
                    item.addEventListener('click', function() {
                        const section = this.getAttribute('data-tech-section');
                        navigateToTechSection(section);
                    });
                });
            }

            // HEADER ACTIVITY-BASED SHOW/HIDE
            function showHeader() {
                if (header && currentScrollPosition > 100) {
                    header.classList.add('scrolled');
                }
            }

            function hideHeaderAfterInactivity() {
                clearTimeout(headerTimeout);
                headerTimeout = setTimeout(() => {
                    // Don't hide header if at the very top of the page (scrollTop = 0)
                    if (header && currentScrollPosition > 0) {
                        header.classList.remove('scrolled');
                    }
                }, 2000); // Hide after 2 seconds of inactivity
            }

            function handleHeaderScroll(event) {
                // Get scroll position from the event target (the page slide that's scrolling)
                const scrollPosition = event && event.target ? event.target.scrollTop : 0;
                currentScrollPosition = scrollPosition;
                
                if (scrollPosition === 0) {
                    // At the very top - show header (desktop only)
                    if (header && window.innerWidth > 768) {
                        header.classList.add('scrolled');
                        hideHeaderAfterInactivity();
                    }
                } else if (scrollPosition > 100) {
                    // Scrolled down - show header and hide after inactivity
                    showHeader();
                    hideHeaderAfterInactivity();
                } else {
                    // Middle zone (1-100px) - hide header
                    if (header) {
                        header.classList.remove('scrolled');
                    }
                }
            }

            function handleMouseMove() {
                // Show header on mouse movement (desktop only)
                if (header && window.innerWidth > 768) {
                    header.classList.add('scrolled');
                    hideHeaderAfterInactivity();
                }
            }

            // Manual header check (for page navigation)
            function checkHeaderOnPageSwitch() {
                const currentPageElement = document.getElementById('page-' + currentPage);
                if (currentPageElement) {
                    const scrollPosition = currentPageElement.scrollTop || 0;
                    currentScrollPosition = scrollPosition;
                    
                    // Show header at the top of a new page (scrollPosition === 0)
                    // This allows the header to be visible when first entering a page
                    if (scrollPosition === 0 && header && window.innerWidth > 768) {
                        header.classList.add('scrolled');
                        hideHeaderAfterInactivity();
                    } else if (scrollPosition > 100) {
                        showHeader();
                        hideHeaderAfterInactivity();
                    } else {
                        // Only hide if we're scrolling in the middle zone (1-100px)
                        if (header && scrollPosition > 0) {
                            header.classList.remove('scrolled');
                        }
                    }
                }
            }

            // Add scroll listeners to all page slides
            document.querySelectorAll('.page-slide').forEach(slide => {
                slide.addEventListener('scroll', handleHeaderScroll);
            });

            // Add mouse move listener
            document.addEventListener('mousemove', handleMouseMove);

            // Initial header state check - show header on first load (desktop only)
            if (header && window.innerWidth > 768) {
                header.classList.add('scrolled');
                hideHeaderAfterInactivity();
            }
            checkHeaderOnPageSwitch();

            // DESKTOP HEADER BACKGROUND SHOW/HIDE
            function showBg() {
                if (header) {
                    header.classList.add('show-bg');
                    clearTimeout(timeout);
                    timeout = setTimeout(() => header.classList.remove('show-bg'), 1000);
                }
            }

            document.addEventListener('mousemove', showBg);
            document.addEventListener('scroll', showBg);

            // ACTIVE SECTION DETECTION (within ABOUT page only)
            const aboutPage = document.getElementById('page-about');
            if (aboutPage) {
                aboutPage.addEventListener('scroll', updateActiveSection);
            }

            function updateActiveSection() {
                if (currentPage !== 'about') return;

                const scroll = aboutPage.scrollTop + 200;
                const sections = aboutPage.querySelectorAll('section[id]');
                
                sections.forEach(section => {
                    const top = section.offsetTop;
                    const height = section.offsetHeight;
                    const id = section.getAttribute('id');

                    if (scroll >= top && scroll < top + height) {
                        document.querySelectorAll('.submenu-item, .mobile-nav-item.subsection').forEach(i => {
                            i.classList.remove('active');
                        });
                        document.querySelectorAll(`[data-section="${id}"]`).forEach(i => {
                            i.classList.add('active');
                        });
                    }
                });
            }

            // KEYBOARD NAVIGATION
            document.addEventListener('keydown', function(e) {
                const pages = ['about', 'ongoing', 'artwork', 'tech', 'services'];
                const currentIndex = pages.indexOf(currentPage);

                if (e.key === 'ArrowRight' && currentIndex < pages.length - 1) {
                    navigateToPage(pages[currentIndex + 1]);
                } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                    navigateToPage(pages[currentIndex - 1]);
                }
            });

            // HANDLE URL HASH ON LOAD
            if (window.location.hash) {
                const hash = window.location.hash.substring(1);
                const pages = ['about', 'ongoing', 'artwork', 'tech', 'services'];
                if (pages.includes(hash)) {
                    navigateToPage(hash);
                }
            }

            // Initial active section check
            updateActiveSection();
            
            // Load about page videos immediately
            loadVideosForPage('about');

            // CONTACT FORM SUBMISSION
            const contactForm = document.getElementById('contact-form');
            if (contactForm) {
                contactForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const submitBtn = contactForm.querySelector('.form-submit');
                    const statusDiv = document.getElementById('form-status');
                    const originalBtnText = submitBtn.textContent;
                    
                    // Disable button and show loading state
                    submitBtn.disabled = true;
                    submitBtn.textContent = 'SENDING...';
                    submitBtn.style.opacity = '0.6';
                    
                    // Get form data
                    const formData = new FormData(contactForm);
                    
                    // Send via fetch
                    fetch('https://freddy-backend-v10h.onrender.com/api/contact', {
                        method: 'POST',
                        body: JSON.stringify(Object.fromEntries(formData)), // Convert FormData to JSON
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Success
                            statusDiv.textContent = data.message;
                            statusDiv.style.color = '#F9FF25';
                            statusDiv.style.display = 'block';
                            contactForm.reset();
                        } else {
                            // Error
                            statusDiv.textContent = data.message;
                            statusDiv.style.color = '#ff4444';
                            statusDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        statusDiv.textContent = 'An error occurred. Please try again or email directly: fmroldanrivero@gmail.com';
                        statusDiv.style.color = '#ff4444';
                        statusDiv.style.display = 'block';
                    })
                    .finally(() => {
                        // Re-enable button
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalBtnText;
                        submitBtn.style.opacity = '1';
                        
                        // Hide status message after 8 seconds
                        setTimeout(() => {
                            statusDiv.style.display = 'none';
                        }, 8000);
                    });
                });
            }
        });