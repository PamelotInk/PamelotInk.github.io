// Simple mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mainContent = document.querySelector('.main-content');
    
    // Sidebar collapse/expand toggle
    if (sidebarToggle) {
        // Check for saved sidebar state
        const sidebarCollapsed = localStorage.getItem('sidebarCollapsed');
        if (sidebarCollapsed === 'true') {
            sidebar.classList.add('collapsed');
        }
        
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            
            // Save preference
            if (sidebar.classList.contains('collapsed')) {
                localStorage.setItem('sidebarCollapsed', 'true');
            } else {
                localStorage.setItem('sidebarCollapsed', 'false');
            }
        });
    }
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            
            // Close sidebar when clicking outside on mobile
            if (sidebar.classList.contains('active')) {
                const closeHandler = function(e) {
                    if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                        sidebar.classList.remove('active');
                        document.removeEventListener('click', closeHandler);
                    }
                };
                
                // Delay to prevent immediate closing
                setTimeout(() => {
                    document.addEventListener('click', closeHandler);
                }, 100);
            }
        });
    }
    
    // Close mobile menu when clicking nav links
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link, .header-nav .header-nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
            
            // Smooth scroll to top for home links
            if (link.getAttribute('href') === '#home') {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Highlight active section in navigation
    const sections = document.querySelectorAll('article[id]');
    const updateActiveNav = function() {
        let scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };
    
    window.addEventListener('scroll', updateActiveNav);
    window.addEventListener('load', updateActiveNav);
    
    // Theme Toggle (Dark Mode / Light Mode)
    const themeToggle = document.getElementById('themeToggle');
    const headerThemeToggle = document.getElementById('headerThemeToggle');
    const darkModeToggle = document.getElementById('darkModeToggle'); // Fallback for old button
    const body = document.body;
    
    // Check for saved dark mode preference
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        body.classList.add('dark-mode');
    }
    
    // Function to toggle theme
    const toggleTheme = function() {
        body.classList.toggle('dark-mode');
        
        // Save preference
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    };
    
    // Toggle theme with header sun/moon button
    if (headerThemeToggle) {
        headerThemeToggle.addEventListener('click', toggleTheme);
    }
    
    // Toggle theme with sidebar sun/moon button
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Fallback for old dark mode button (if it exists)
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleTheme);
    }

    // ============================================
    // 3D Floating Data Elements - Mouse Interaction
    // ============================================
    const data3dContainer = document.getElementById('data3dContainer');
    const dataElements = document.querySelectorAll('.data-element');
    
    if (data3dContainer && dataElements.length > 0) {
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        let targetX = mouseX;
        let targetY = mouseY;
        let time = 0;
        
        // Track mouse position
        document.addEventListener('mousemove', function(e) {
            targetX = e.clientX;
            targetY = e.clientY;
        });
        
        // Smooth animation loop
        function animate3DElements() {
            time += 0.01;
            
            // Smooth lerp towards target
            mouseX += (targetX - mouseX) * 0.08;
            mouseY += (targetY - mouseY) * 0.08;
            
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;
            
            dataElements.forEach((element, index) => {
                const speed = parseFloat(element.dataset.speed) || 0.02;
                
                // Base idle floating motion
                const idleX = Math.sin(time + index * 0.5) * 10;
                const idleY = Math.cos(time * 0.8 + index * 0.7) * 8;
                
                // Mouse-based offset (parallax effect)
                const mouseOffsetX = (mouseX - centerX) * speed * 80;
                const mouseOffsetY = (mouseY - centerY) * speed * 80;
                
                // Combined offset
                const offsetX = idleX + mouseOffsetX;
                const offsetY = idleY + mouseOffsetY;
                
                // 3D rotation based on mouse position
                const rotateY = (mouseX - centerX) * speed * 0.8;
                const rotateX = -(mouseY - centerY) * speed * 0.8;
                
                // Depth effect
                const translateZ = 30 + Math.sin(time + index) * 20;
                
                element.style.transform = `
                    translateX(${offsetX}px) 
                    translateY(${offsetY}px) 
                    translateZ(${translateZ}px) 
                    rotateX(${rotateX}deg) 
                    rotateY(${rotateY}deg)
                    scale(${1 + speed * 2})
                `;
            });
            
            requestAnimationFrame(animate3DElements);
        }
        
        animate3DElements();
    }
});
