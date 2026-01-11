const { chromium } = require("playwright");

(async () => {
  const url = process.env.APP_URL;
  if (!url) throw new Error("APP_URL is not set");

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const target = `${url}/?wake=${Date.now()}`;
  console.log("Opening:", target);

  await page.goto(target, { waitUntil: "domcontentloaded", timeout: 60000 });

  const wakeBtn = page.getByRole("button", { name: /get this app back up/i });

  if (await wakeBtn.count()) {
    console.log("Wake button found. Clicking...");
    await wakeBtn.first().click();
    await page.waitForTimeout(15000);
  } else {
    console.log("Wake button not found. App likely already awake.");
  }

  await browser.close();
})();
