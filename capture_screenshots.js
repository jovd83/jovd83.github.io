import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Papa from 'papaparse';

// Add stealth plugin to evade detection
puppeteer.use(StealthPlugin());

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Config for multiple files
const TARGETS = [
    {
        csvPath: path.join(__dirname, 'public', 'data', 'tools.csv'),
        imgDir: path.join(__dirname, 'public', 'img', 'tools'),
        baseUrl: '/jovd83_github_page/img/tools/',
        urlField: 'Website URL',
        fallbackUrlFields: ['Link', 'link_primary'],
        titleField: 'Title'
    },
    {
        csvPath: path.join(__dirname, 'public', 'data', 'blogs.csv'),
        imgDir: path.join(__dirname, 'public', 'img', 'blogs'),
        baseUrl: '/jovd83_github_page/img/blogs/',
        urlField: 'link_primary',
        fallbackUrlFields: ['Link', 'Website URL'],
        titleField: 'title'
    },
    {
        csvPath: path.join(__dirname, 'public', 'data', 'benchmarks.csv'),
        imgDir: path.join(__dirname, 'public', 'img', 'benchmarks'),
        baseUrl: '/jovd83_github_page/img/benchmarks/',
        urlField: 'link_primary',
        fallbackUrlFields: ['Link', 'Website URL'],
        titleField: 'title'
    },
    {
        csvPath: path.join(__dirname, 'public', 'data', 'prompt_frameworks.csv'),
        imgDir: path.join(__dirname, 'public', 'img', 'prompt_frameworks'),
        baseUrl: '/jovd83_github_page/img/prompt_frameworks/',
        urlField: 'URL to explanation',
        fallbackUrlFields: ['Link', 'Website URL'],
        titleField: 'Name'
    },
    {
        csvPath: path.join(__dirname, 'public', 'data', 'extratools.csv'),
        imgDir: path.join(__dirname, 'public', 'img', 'extratools'),
        baseUrl: '/jovd83_github_page/img/extratools/',
        urlField: 'Website URL',
        fallbackUrlFields: ['Link', 'link_primary'],
        titleField: 'Title'
    }
];

async function captureScreenshotsForTarget(browser, target) {
    console.log(`\nProcessing ${path.basename(target.csvPath)}...`);

    // Ensure output directory exists
    if (!fs.existsSync(target.imgDir)) {
        fs.mkdirSync(target.imgDir, { recursive: true });
    }

    // Read and Parse CSV
    const csvContent = fs.readFileSync(target.csvPath, 'utf-8');
    const parseResult = Papa.parse(csvContent, {
        header: true,
        skipEmptyLines: true
    });

    if (parseResult.errors.length > 0) {
        console.error('CSV Parding Errors:', parseResult.errors);
    }

    const data = parseResult.data;

    for (let i = 0; i < data.length; i++) {
        const row = data[i];

        // Find URL
        let url = row[target.urlField];
        if (!url && target.fallbackUrlFields) {
            for (const field of target.fallbackUrlFields) {
                if (row[field]) {
                    url = row[field];
                    break;
                }
            }
        }

        const title = row[target.titleField] || `item_${i}`;

        if (!url || !url.startsWith('http')) {
            console.log(`  Skipping invalid URL for: ${title}`);
            continue;
        }

        // Sanitize filename
        const filename = title.toLowerCase().replace(/[^a-z0-9]/g, '_') + '.png';
        const outputPath = path.join(target.imgDir, filename);
        const publicPath = target.baseUrl + filename;

        // Check if image already exists
        if (fs.existsSync(outputPath)) {
            console.log(`  Skipping existing: ${filename}`);
            row['image_url'] = publicPath; // Ensure CSV has it
            continue;
        }

        console.log(`  [${i + 1}/${data.length}]: ${title} -> ${url}`);

        try {
            const page = await browser.newPage();

            // Set a realistic viewport 
            await page.setViewport({ width: 1366, height: 768 });

            // Navigate
            await page.goto(url, {
                waitUntil: 'networkidle2',
                timeout: 30000
            });

            // Random delay
            await new Promise(r => setTimeout(r, 2000));

            // Screenshot
            await page.screenshot({ path: outputPath });

            // Update CSV Row
            row['image_url'] = publicPath;
            // console.log(`    Saved to ${outputPath}`); 

            await page.close();

        } catch (err) {
            console.error(`    Failed to capture ${url}: ${err.message}`);
        }
    }

    // Write back to CSV
    const newCsvContent = Papa.unparse(data, {
        quotes: true,
        quoteChar: '"',
        escapeChar: '"',
        delimiter: ",",
        header: true,
        newline: "\r\n",
    });

    fs.writeFileSync(target.csvPath, newCsvContent);
    console.log(`Updated ${path.basename(target.csvPath)} with new screenshot paths.`);
}

async function run() {
    console.log('Starting STEALTH screenshot capture for multiple files...');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--window-size=1920,1080'
        ]
    });

    for (const target of TARGETS) {
        await captureScreenshotsForTarget(browser, target);
    }

    await browser.close();
    console.log('All done!');
}

run();
