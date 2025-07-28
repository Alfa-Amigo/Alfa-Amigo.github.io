document.addEventListener('DOMContentLoaded', function() {
    // Efecto de selección de respuestas
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Solo para demostración - en una app real esto vendría del backend
            const isCorrect = this.dataset.correct === 'true';
            
            if (isCorrect) {
                this.classList.add('correct');
                // Animación de puntos ganados
                const xpBadge = document.querySelector('.xp-badge');
                if (xpBadge) {
                    xpBadge.classList.add('xp-animation');
                    setTimeout(() => {
                        xpBadge.classList.remove('xp-animation');
                    }, 500);
                }
            } else {
                this.classList.add('incorrect');
            }
            
            // Deshabilitar todos los botones después de seleccionar
            document.querySelectorAll('.option-btn').forEach(b => {
                b.disabled = true;
            });
            
            // Mostrar feedback
            const feedback = document.createElement('div');
            feedback.className = `alert ${isCorrect ? 'alert-success' : 'alert-danger'} mt-3`;
            feedback.textContent = isCorrect ? '¡Correcto! +10 XP' : 'Incorrecto, intenta nuevamente';
            this.parentNode.appendChild(feedback);
        });
    });
    
    // Efecto de carga para las lecciones
    const lessonCards = document.querySelectorAll('.lesson-card');
    lessonCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
