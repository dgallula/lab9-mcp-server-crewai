import axios from "axios";

const ids = [1, 2, 5, 7];

async function fetchName(id) {
  try {
    const resp = await axios.get(`https://jsonplaceholder.typicode.com/users/${id}`);
    return resp.data && resp.data.name ? resp.data.name : null;
  } catch (err) {
    console.error(`Failed to fetch id=${id}:`, err.message || err);
    return null;
  }
}

async function main() {
  const names = [];
  for (const id of ids) {
    const name = await fetchName(id);
    names.push(name);
  }
  console.log(names);
}

main();
