const express = require('express');
const cors = require('cors');
const ytdl = require('@distube/ytdl-core');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Test route
app.get('/', (req, res) => {
    res.send("Tech With Dasun Downloader API is running successfully!");
});

// Download info route
app.get('/download', async (req, res) => {
    try {
        const videoURL = req.query.url;
        if (!videoURL || !ytdl.validateURL(videoURL)) {
            return res.status(400).json({ success: false, error: 'කරුණාකර సరైన YouTube URL එකක් ලබා දෙන්න!' });
        }

        const info = await ytdl.getInfo(videoURL);
        const title = info.videoDetails.title;
        const thumbnail = info.videoDetails.thumbnails[info.videoDetails.thumbnails.length - 1].url;
        
        // formats get (video and audio)
        const formats = ytdl.filterFormats(info.formats, 'videoandaudio');
        
        res.json({
            success: true,
            title: title,
            thumbnail: thumbnail,
            formats: formats.map(f => ({
                quality: f.qualityLabel || 'Standard',
                container: f.container,
                url: f.url
            }))
        });

    } catch (error) {
        console.error("Error details:", error);
        res.status(500).json({ success: false, error: 'YouTube මඟින් මෙම වීඩියෝව අවහිර කර ඇත හෝ සර්වර් දෝෂයකි.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
