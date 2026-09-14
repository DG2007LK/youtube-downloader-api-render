const express = require('express');
const cors = require('cors');
const ytdl = require('ytdl-core');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Test route
app.get('/', (req, res) => {
    name = "Tech With Dasun Downloader API is running successfully!";
    res.send(name);
});

// Download info route
app.get('/download', async (req, res) => {
    try {
        const videoURL = req.query.url;
        if (!videoURL || !ytdl.validateURL(videoURL)) {
            return res.status(400).json({ error: 'කරුණාකර సరైన YouTube URL එකක් ලබා දෙන්න!' });
        }

        const info = await ytdl.getInfo(videoURL);
        const title = info.videoDetails.title;
        const thumbnail = info.videoDetails.thumbnails[info.videoDetails.thumbnails.length - 1].url;
        
        // formats get
        const formats = ytdl.filterFormats(info.formats, 'videoandaudio');
        
        res.json({
            success: true,
            title: title,
            thumbnail: thumbnail,
            formats: formats.map(f => ({
                quality: f.qualityLabel,
                container: f.container,
                url: f.url
            }))
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'වීඩියෝ විස්තර ලබාගැනීමේදී දෝෂයක් සිදු විය.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
