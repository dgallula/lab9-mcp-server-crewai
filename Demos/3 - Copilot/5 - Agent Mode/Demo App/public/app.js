let currentMood = '';

function selectMood(mood) {
  currentMood = mood;
  fetchRecipe(mood);
}

function fetchRecipe(mood) {
  // Show loading
  document.getElementById('moodSelection').classList.add('hidden');
  document.getElementById('recipeDisplay').classList.add('hidden');
  document.getElementById('loading').classList.remove('hidden');

  // Fetch recipe from API
  fetch(`http://localhost:3001/api/recipe/${mood}`)
    .then(response => response.json())
    .then(data => {
      displayRecipe(data);
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Failed to fetch recipe. Please try again.');
      backToMoods();
    });
}

function displayRecipe(recipe) {
  // Hide loading
  document.getElementById('loading').classList.add('hidden');
  
  // Display recipe
  document.getElementById('recipeName').textContent = recipe.name;
  document.getElementById('recipeIngredients').textContent = recipe.ingredients;
  document.getElementById('recipeInstructions').textContent = recipe.instructions;
  document.getElementById('recipeDisplay').classList.remove('hidden');
}

function getNewRecipe() {
  if (currentMood) {
    fetchRecipe(currentMood);
  }
}

function backToMoods() {
  document.getElementById('recipeDisplay').classList.add('hidden');
  document.getElementById('loading').classList.add('hidden');
  document.getElementById('moodSelection').classList.remove('hidden');
  currentMood = '';
}
