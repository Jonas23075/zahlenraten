document.addEventListener('DOMContentLoaded', function() {
    const guessForm = document.getElementById('guess-form');
    const guessInput = document.getElementById('guess');
    const feedback = document.getElementById('feedback');
    const attempts = document.getElementById('attempts');
    const gameOver = document.getElementById('game-over');
    const saveScoreForm = document.getElementById('save-score-form');
    
    let attemptsCount = 0;
    
    if (guessForm) {
        guessForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const guess = parseInt(guessInput.value);
            if (isNaN(guess)) {
                feedback.textContent = 'Bitte gib eine gültige Zahl ein!';
                return;
            }
            
            attemptsCount++;
            attempts.textContent = attemptsCount;
            
            fetch('/game/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ guess: guess }),
            })
            .then(response => response.json())
            .then(data => {
                feedback.textContent = data.message;
                
                if (data.correct) {
                    guessForm.style.display = 'none';
                    gameOver.style.display = 'block';
                    document.getElementById('final-score').textContent = attemptsCount;
                    document.getElementById('score-value').value = attemptsCount;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                feedback.textContent = 'Ein Fehler ist aufgetreten. Bitte versuche es erneut.';
            });
            
            guessInput.value = '';
            guessInput.focus();
        });
    }
    
    if (saveScoreForm) {
        saveScoreForm.addEventListener('submit', function(e) {
            if (!document.getElementById('player-name').value.trim()) {
                e.preventDefault();
                alert('Bitte gib deinen Namen ein!');
            }
        });
    }
});
