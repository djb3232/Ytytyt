// Main JavaScript for Multi-Format Downloader

document.addEventListener('DOMContentLoaded', function() {
    // Handle audio-only checkbox
    const audioOnlyCheckbox = document.getElementById('audio_only');
    const formatSelect = document.getElementById('format');
    
    if (audioOnlyCheckbox && formatSelect) {
        audioOnlyCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Filter to only show audio formats
                const audioFormats = ['auto', 'mp3', 'm4a', 'opus', 'wav', 'flac'];
                
                // Save current selection if possible
                const currentValue = formatSelect.value;
                
                // Clear options
                formatSelect.innerHTML = '';
                
                // Add audio options
                audioFormats.forEach(format => {
                    const option = document.createElement('option');
                    option.value = format;
                    option.textContent = format === 'auto' ? 'Auto' : format.toUpperCase();
                    formatSelect.appendChild(option);
                });
                
                // Restore selection if it's an audio format
                if (audioFormats.includes(currentValue)) {
                    formatSelect.value = currentValue;
                }
            } else {
                // Restore all formats
                const allFormats = [
                    {value: 'auto', text: 'Auto'},
                    {value: 'mp4', text: 'MP4'},
                    {value: 'webm', text: 'WebM'},
                    {value: 'mkv', text: 'MKV'},
                    {value: 'mp3', text: 'MP3'},
                    {value: 'm4a', text: 'M4A'},
                    {value: 'opus', text: 'Opus'},
                    {value: 'wav', text: 'WAV'},
                    {value: 'flac', text: 'FLAC'}
                ];
                
                // Save current selection if possible
                const currentValue = formatSelect.value;
                
                // Clear options
                formatSelect.innerHTML = '';
                
                // Add all options
                allFormats.forEach(format => {
                    const option = document.createElement('option');
                    option.value = format.value;
                    option.textContent = format.text;
                    formatSelect.appendChild(option);
                });
                
                // Restore selection
                formatSelect.value = currentValue;
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});