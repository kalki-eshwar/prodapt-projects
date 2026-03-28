import { test, expect } from '@playwright/test';

test.describe('Event Booking System', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('Successful Booking reduces seats and shows summary', async ({ page }) => {
    // Select Reack Workshop (id: 1)
    await page.getByTestId('select-event').selectOption('1');
    await page.getByTestId('input-name').fill('Anjali');
    await page.getByTestId('input-seats').fill('2');
    
    await page.getByTestId('btn-book').click();

    // Verify confirmation message details
    const summary = page.getByTestId('booking-summary');
    await expect(summary).toBeVisible();
    await expect(summary).toContainText('Name: Anjali');
    await expect(summary).toContainText('Event: React Workshop');
    await expect(summary).toContainText('Seats Booked: 2');
    await expect(summary).toContainText('Remaining Seats: 18');

    // Verify the listed available seats are updated
    const eventCard = page.getByTestId('event-card-1');
    await expect(eventCard).toContainText('Seats Available: 18');
  });

  test('Validation Error on empty form submission', async ({ page }) => {
    // Click book without filling any details
    await page.getByTestId('btn-book').click();
    
    // View error message
    const error = page.getByTestId('error-message');
    await expect(error).toBeVisible();
    await expect(error).toContainText('All fields are required');
  });

  test('Validation Error on overbooking', async ({ page }) => {
    // Select Cloud Training which has 10 seats initially
    await page.getByTestId('select-event').selectOption('3');
    await page.getByTestId('input-name').fill('John');
    await page.getByTestId('input-seats').fill('12'); // More than 10
    
    await page.getByTestId('btn-book').click();

    // Verify it shows error and doesn't book
    const error = page.getByTestId('error-message');
    await expect(error).toBeVisible();
    await expect(error).toContainText('Not enough seats available');
  });

  test('Edge Case with 0 Seats (Sold Out)', async ({ page }) => {
    // Event 4 is Soldier Out explicitly for testing edge cases
    await page.getByTestId('select-event').selectOption('4');
    
    // Check that button is disabled
    const bookButton = page.getByTestId('btn-book');
    await expect(bookButton).toBeDisabled();
    
    const card = page.getByTestId('event-card-4');
    await expect(card).toContainText('Sold Out');
  });
});