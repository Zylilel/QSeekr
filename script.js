console.log('JS Connected')

async function handleSearch() {
    console.log('Search triggered!');

    try {
        const file = document.getElementById('imageUpload').files[0];
        const text = document.getElementById('textInput').value;

        console.log('File:', file);
        console.log('Text:', text);

        const formData = new FormData();
        if (file) {
            formData.append('file', file);
        }
        if (text) {
            formData.append('query', text);
        }

        console.log('Sending request...');

        const response = await fetch('http://localhost:8000/search', {
            method: 'POST',
            body: formData
        });

        console.log('Response status:', response.status);

        const data = await response.json();
        console.log('Response data:', data);

        // Display results
        let html = `<h3>Query: ${data.query}</h3>`;

        if (data.results && data.results.length > 0) {
            html += `<p>Found ${data.results.length} results:</p>`;

            data.results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <h4>Result ${index + 1} (Match: ${result.score}%)</h4>
                        <p><strong>Subject:</strong> ${result.subject}</p>
                        <p><strong>Topic:</strong> ${result.topic}</p>
                        <p><strong>Question ID:</strong> ${result.id}</p>
                        <p><strong>Question:</strong> ${result.question_text.substring(0, 300)}...</p>
                        ${result.question_images && result.question_images.length > 0 ?
                            `<p><strong>Question Images:</strong> ${result.question_images.length} image(s)</p>` : ''}
                        ${result.markscheme_images && result.markscheme_images.length > 0 ?
                            `<p><strong>Answer Images:</strong> ${result.markscheme_images.length} image(s)</p>` : ''}
                    </div>
                `;
            });
        } else {
            html += '<p>No results found.</p>';
        }

        document.getElementById('result').innerHTML = html;
    } catch (error) {
        console.error('FULL Error:', error);
        console.error('Error stack:', error.stack);
        document.getElementById('result').innerHTML = `<h3>Error: ${error.message}</h3>`;
    }
}

document.getElementById('sendBtn').addEventListener('click', handleSearch);

document.getElementById('textInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        handleSearch();
    }
});

document.getElementById('imageUpload').addEventListener('change', function() {
    if (this.files[0]) {
        handleSearch();
    }
});