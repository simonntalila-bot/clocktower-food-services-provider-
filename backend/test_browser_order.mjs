export default async function run(page, ui) {
  // Fill name
  await page.locator('input[name="name"]').fill('Browser Test Mteja');
  
  // Fill phone
  await page.locator('input[name="phone"]').fill('0712345678');
  
  // Fill email (optional)
  await page.locator('input[name="email"]').fill('browser@test.com');
  
  // Fill table (optional)
  await page.locator('input[name="table_location"]').fill('Meza 99');
  
  // Select payment method - Cash
  await page.locator('select[name="payment_method"]').selectOption('cash');
  
  // Set quantity for first food item
  const firstQty = page.locator('input[type="number"]').first();
  await firstQty.fill('2');
  
  // Fill comments
  await page.locator('textarea[name="comments"]').fill('Testing from browser automation');
  
  // Take snapshot before submit
  const before = await ui.snapshot();
  
  // Submit
  await page.locator('button[type="submit"]').click();
  
  // Wait for response
  await page.waitForTimeout(2000);
  
  // Take snapshot after submit
  const after = await ui.snapshot();
  
  const success = after.includes('Asante') || after.includes('Agizo') || after.includes('CTF-');
  
  return {
    success,
    pageText: after.substring(0, 500),
    url: page.url()
  };
}
