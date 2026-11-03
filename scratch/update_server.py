with open('server.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});"""

addition = """app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

// 取得檔案路徑資訊 (供 Outlook 複製貼上使用)
app.get('/api/file-path', (req, res) => {
    try {
        let relPath = req.query.path || '';
        if (!relPath) {
            return res.status(400).json({ error: 'Missing path parameter' });
        }
        relPath = decodeURIComponent(relPath).replace(/^\.?\/+/, '');
        const localFullPath = path.resolve(__dirname, relPath);
        if (!fs.existsSync(localFullPath)) {
            return res.status(404).json({ error: 'File not found on local disk', path: localFullPath });
        }
        return res.json({
            relPath: relPath,
            fullPath: localFullPath,
            filename: path.basename(localFullPath),
            fileUrl: `file:///${localFullPath.replace(/\\/g, '/')}`
        });
    } catch (e) {
        return res.status(500).json({ error: e.message });
    }
});"""

if target in text:
    text = text.replace(target, addition)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("server.js updated successfully!")
else:
    print("target not found in server.js")

