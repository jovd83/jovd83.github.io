
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const HTML_FILE = path.resolve('shownotes/GenZ_AILiteracy/index.html');

async function main() {
    console.log(`Processing ${HTML_FILE}...`);

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Load the local HTML file
    const fileUrl = 'file://' + HTML_FILE.replace(/\\/g, '/');
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });

    // 1. Add IDs to Part Headers for TOC
    await page.evaluate(() => {
        const headers = Array.from(document.querySelectorAll('h2.section-title'));
        headers.forEach((h2) => {
            const text = h2.textContent.trim().toLowerCase();
            if (text.includes('part 1') || text.includes('part i:')) h2.id = 'part1';
            else if (text.includes('part ii') || text.includes('part 2')) h2.id = 'part2';
            else if (text.includes('part iii') || text.includes('part 3')) h2.id = 'part3';
            else if (text.includes('part iv') || text.includes('part 4')) h2.id = 'part4';
            else if (text.includes('part v') || text.includes('part 5')) h2.id = 'part5';
            else if (text.includes('part vi') || text.includes('part 6')) h2.id = 'part6';
            else if (text.includes('part vii') || text.includes('part 7')) h2.id = 'part7';
        });
    });

    // 2. Identify generic links
    const linksToEnrich = await page.evaluate(() => {
        const anchors = Array.from(document.querySelectorAll('a'));
        return anchors.map((a, index) => {
            const text = a.textContent.trim();
            const href = a.href;

            // Check if text is generic "Link" or similar
            const isGeneric = text.toLowerCase() === 'link' || text.toLowerCase() === 'watch video' || text === href;

            if (isGeneric && href && !href.startsWith('mailto:') && !href.startsWith('file:')) {
                // Return index to identify element later
                return { index, href, isYoutube: (href.includes('youtube.com') || href.includes('youtu.be')) };
            }
            return null;
        }).filter(item => item !== null);
    });

    console.log(`Found ${linksToEnrich.length} links to enrich.`);

    // 3. Process links
    for (const link of linksToEnrich) {
        let newTitle = '';

        if (link.isYoutube) {
            try {
                // Fetch YouTube Title
                console.log(`Fetching YouTube title for: ${link.href}`);
                const ytPage = await browser.newPage();
                await ytPage.goto(link.href, { waitUntil: 'domcontentloaded' });
                newTitle = await ytPage.title();
                await ytPage.close();

                // Clean up title (remove "- YouTube")
                newTitle = newTitle.replace(/- YouTube$/, '').trim();
                console.log(`  -> Title: ${newTitle}`);
            } catch (e) {
                console.error(`  Failed to fetch title for ${link.href}: ${e.message}`);
                newTitle = 'Watch Video';
            }
        } else {
            // Slug to Title conversion
            try {
                const urlObj = new URL(link.href);
                let slug = urlObj.pathname.split('/').filter(p => p).pop();
                if (!slug) slug = urlObj.hostname;

                // Remove extension
                if (slug.includes('.')) slug = slug.split('.').slice(0, -1).join('.');

                // Simple cleanup
                newTitle = slug.replace(/[-_]/g, ' ');
                // Title case
                newTitle = newTitle.replace(/\b\w/g, c => c.toUpperCase());

                if (newTitle.length < 3) newTitle = "Read Article";

                console.log(`  Converted slug for ${link.href} -> ${newTitle}`);
            } catch (e) {
                newTitle = 'Read Article';
            }
        }

        // Update the link in the page context
        if (newTitle) {
            await page.evaluate((index, title) => {
                const anchors = Array.from(document.querySelectorAll('a'));
                const a = anchors[index];
                if (a) {
                    // Update text content of span if exists (for video cards)
                    const span = a.querySelector('span');
                    if (span) span.textContent = title;
                    else a.textContent = title;

                    // Update alt text of image if generic
                    const img = a.querySelector('img');
                    if (img && (img.alt === 'Link' || img.alt === '')) img.alt = title;
                }
            }, link.index, newTitle);
        }
    }

    // 4. Save modified HTML
    const content = await page.content();
    fs.writeFileSync(HTML_FILE, content);
    console.log('Saved updated HTML.');

    await browser.close();
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
