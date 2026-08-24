const fs = require('fs');

const indexPath = 'c:/Users/MARCO/OneDrive/Desktop/J/vscode/attech0818/index.html';
const content = fs.readFileSync(indexPath, 'utf8');

// Find where <script> starts after line 1650
const scriptStartIdx = content.indexOf('<script>\r\n    document.getElementById(\'year\')') !== -1 
    ? content.indexOf('<script>\r\n    document.getElementById(\'year\')')
    : content.indexOf('<script>\n    document.getElementById(\'year\')');

if (scriptStartIdx === -1) {
    console.error('Could not find script start');
    process.exit(1);
}

const htmlBefore = content.substring(0, scriptStartIdx);

const modularScriptTags = `    <!-- ==========================================
         前端模組化 JavaScript 腳本庫
         ========================================== -->
    <script src="js/state.js"></script>
    <script src="js/search-engine.js"></script>
    <script src="js/data-repo.js"></script>
    <script src="js/filter-engine.js"></script>
    <script src="js/table-renderer.js"></script>
    <script src="js/compare.js"></script>
    <script src="js/contact.js"></script>
    <script src="js/router.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
`;

const updatedContent = htmlBefore + modularScriptTags;
fs.writeFileSync(indexPath, updatedContent, 'utf8');
console.log('✅ Successfully updated index.html with modular script imports!');
