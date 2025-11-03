// Snowfall animation script
(function() {
    function createSnowflake() {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.innerHTML = '❄';
        snowflake.style.left = Math.random() * 100 + '%';
        snowflake.style.animationDuration = (Math.random() * 3 + 2) + 's';
        snowflake.style.fontSize = (Math.random() * 10 + 10) + 'px';
        snowflake.style.opacity = Math.random();
        return snowflake;
    }

    function initSnow() {
        const snowContainer = document.getElementById('snow');
        if (!snowContainer) return;

        // Create 50 snowflakes
        for (let i = 0; i < 50; i++) {
            const snowflake = createSnowflake();
            snowflake.style.animationDelay = Math.random() * 5 + 's';
            snowContainer.appendChild(snowflake);
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSnow);
    } else {
        initSnow();
    }
})();

