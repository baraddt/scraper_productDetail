const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const url = process.argv[2];

if (!url) {
    console.error("URL tidak diberikan.\nJalankan dengan: node scraper_shopee.js <URL>");
    process.exit(1);
}

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    let productData = null;

    page.on("response", async (response) => {
        try {
            const reqUrl = response.url();
            if (reqUrl.includes("/api/v4/pdp/get_pc")) {
                const json = await response.json();
                productData = json;
            }
        } catch (err) {
            console.error("Gagal parsing response Shopee:", err.message);
        }
    });

    try {
        await page.goto(url, { waitUntil: "networkidle2" });
        await page.waitForTimeout(7000);
    } catch (err) {
        console.error("Gagal buka halaman Shopee:", err.message);
        console.log("{}");
        await browser.close();
        process.exit(1);
    }

    if (productData) {
        console.log(JSON.stringify(productData));
    } else {
        console.error("Tidak menemukan data dari /get_pc");
    }

    await browser.close();
})();
