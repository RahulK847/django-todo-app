const advancedBtn = document.getElementById('advanced-btn');
const advancedSettings = document.getElementById('advanced-settings');

advancedBtn.addEventListener('click', () => {
    if (advancedSettings.style.display === 'none') {
        advancedSettings.style.display = 'block';
    } else {
        advancedSettings.style.display = 'none';
    }});