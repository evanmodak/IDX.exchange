const resultsElement = document.getElementById('results');

// get bookmarks
chrome.bookmarks.getTree((tree) => {
    const bookmarks = [];

    function extractBookmarks(nodes) {
        for (const node of nodes) {
            if (node.url) {
                bookmarks.push ({
                    title: node.title,
                    url: node.url
                });
            }
            if (node.children) {
                extractBookmarks(node.children);
            }
        }
    }
    
    extractBookmarks(tree);
    for (let b of bookmarks) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        
        a.textContent = b.title;
        a.href = b.url;
        a.target = '_blank';
        
        li.appendChild(a);
        resultsElement.appendChild(li);
    }
                });
            
