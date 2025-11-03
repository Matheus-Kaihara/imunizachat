document.addEventListener("DOMContentLoaded", () => {

    
    const sectionsToAnimate = document.querySelectorAll('.content-section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, {
        threshold: 0.1
    });
    sectionsToAnimate.forEach(section => {
        observer.observe(section);
    });


    
    const mainNav = document.querySelector('.main-nav'); 
    const navLinks = document.querySelectorAll('.main-nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            
            if (mainNav.classList.contains('is-open')) {
                mainNav.classList.remove('is-open');
            }
        });
    });

    
    // --- LÓGICA DO MENU HAMBÚRGUER --- 
    const hamburgerButton = document.getElementById('hamburger-button');

    hamburgerButton.addEventListener('click', () => {
        mainNav.classList.toggle('is-open');
    });

    
// --- LÓGICA DO CARROSSEL DE IMAGENS (COM AUTO-PLAY) ---
    const carouselContainer = document.querySelector('.carousel-container');

   
    if (carouselContainer) {
        const carouselTrack = carouselContainer.querySelector('.carousel-track');
        const carouselImages = carouselContainer.querySelectorAll('.carousel-track img');
        const prevButton = carouselContainer.querySelector('.carousel-button.prev');
        const nextButton = carouselContainer.querySelector('.carousel-button.next');
        
        let currentIndex = 0;
        const imagesPerPage = 3; 
        const totalImages = carouselImages.length;
        let autoPlayInterval; 
        
        const updateCarousel = () => {
            if (totalImages === 0) return;
            const imageWidth = carouselImages[0].offsetWidth + 20;
            carouselTrack.style.transform = `translateX(${-currentIndex * imageWidth}px)`;
            
           
            prevButton.disabled = currentIndex === 0;
            nextButton.disabled = currentIndex >= (totalImages - imagesPerPage);
        };

        
        const slideNext = () => {
            
            if (currentIndex >= (totalImages - imagesPerPage)) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }
            updateCarousel();
        };
        
        
        const startAutoPlay = () => {
            
            clearInterval(autoPlayInterval);
            autoPlayInterval = setInterval(slideNext, 3000); 
        };

        // Função para parar o auto-play
        const stopAutoPlay = () => {
            clearInterval(autoPlayInterval);
        };

        
        prevButton.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });

        nextButton.addEventListener('click', () => {
            if (currentIndex < (totalImages - imagesPerPage)) {
                currentIndex++;
                updateCarousel();
            }
        });

        
        carouselContainer.addEventListener('mouseenter', stopAutoPlay);
        carouselContainer.addEventListener('mouseleave', startAutoPlay);
        
      
        prevButton.addEventListener('click', () => { stopAutoPlay(); startAutoPlay(); });
        nextButton.addEventListener('click', () => { stopAutoPlay(); startAutoPlay(); });

        
        window.addEventListener('resize', updateCarousel);
        
        
        updateCarousel();
        startAutoPlay();
    }
});