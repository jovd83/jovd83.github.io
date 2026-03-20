import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import path from 'path';

puppeteer.use(StealthPlugin());

const urls = [
    { url: 'https://wisprflow.ai/', path: 'public/img/tools/wispr_flow.png' },
    { url: 'https://agentskills.io/', path: 'public/img/tools/agentskills.png' },
    { url: 'https://stitch.withgoogle.com/', path: 'public/img/tools/google_stitch.png' },
    { url: 'https://github.com/vercel-labs/skills', path: 'public/img/libraries/npx_skills.png' },
    { url: 'https://github.com/agentskills/agentskills', path: 'public/img/libraries/agentskills_lib.png' }
];

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    for (const item of urls) {
        console.log(`Processing ${item.url}...`);
        try {
            await page.goto(item.url, { waitUntil: 'networkidle2', timeout: 30000 });
            
            // Get title and description
            const info = await page.evaluate(() => {
                const title = document.title;
                const metaDesc = document.querySelector('meta[name="description"]')?.content || '';
                return { title, metaDesc };
            });
            console.log(`Title: ${info.title}\nDescription: ${info.metaDesc}`);
            
            // Take screenshot
            await page.screenshot({ path: path.join(process.cwd(), item.path) });
            console.log(`Saved screenshot to ${item.path}`);
        } catch (err) {
            console.error(`Failed on ${item.url}:`, err.message);
        }
    }
    
    await browser.close();
})();
