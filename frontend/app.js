const axios = require('axios');
const readline = require('readline');
const fs = require('fs');
const FormData = require('form-data');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
let basket = [];

function prompt(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function searchProduct() {
  const query = await prompt('Enter product to search: ');
  try {
    const res = await axios.get(`http://127.0.0.1:8000/compare/${encodeURIComponent(query)}`);
    console.log('Price Comparison:');
    res.data.comparisons.forEach(c => console.log(`${c.store}: R${c.price}`));
  } catch (err) { console.error('Error:', err.response ? err.response.data : err.message); }
}

async function addToBasket() {
  const name = await prompt('Enter product name: ');
  const qtyStr = await prompt('Enter quantity: ');
  const qty = parseFloat(qtyStr) || 1;
  basket.push({ name, qty });
  console.log(`Added ${name} x${qty} to basket.`);
}

async function uploadReceipt() {
  const filePath = await prompt('Enter receipt image path: ');
  const storeName = await prompt('Enter store name: ');
  if (!fs.existsSync(filePath)) { console.error('File not found'); return; }
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));
  form.append('store_name', storeName);
  try {
    const res = await axios.post('http://127.0.0.1:8000/upload_receipt', form, { headers: form.getHeaders() });
    console.log(res.data.message);
  } catch (err) { console.error('Upload failed:', err.response ? err.response.data : err.message); }
}

async function mainMenu() {
  console.log('\\nGrocery Price Tracker CLI');
  console.log('1. Search product');
  console.log('2. Add product to basket');
  console.log('3. Upload receipt');
  console.log('4. Exit');
  const choice = await prompt('Choose option: ');
  switch (choice.trim()) {
    case '1': await searchProduct(); break;
    case '2': await addToBasket(); break;
    case '3': await uploadReceipt(); break;
    case '4': rl.close(); return;
    default: console.log('Invalid option');
  }
  mainMenu();
}

mainMenu();

