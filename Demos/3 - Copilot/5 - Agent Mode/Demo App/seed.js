const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./recipes.db');

db.serialize(() => {
  // Create recipes table
  db.run(`CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT NOT NULL,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
  )`);

  // Clear existing data
  db.run('DELETE FROM recipes');

  // Sample recipes for different moods
  const recipes = [
    // Happy recipes
    { mood: 'happy', name: 'Rainbow Fruit Salad', ingredients: 'Mixed berries, Mango, Kiwi, Orange, Honey', instructions: 'Chop all fruits into bite-sized pieces. Mix in a bowl and drizzle with honey. Serve chilled.' },
    { mood: 'happy', name: 'Celebration Pancakes', ingredients: 'Flour, Eggs, Milk, Sugar, Butter, Sprinkles', instructions: 'Mix flour, eggs, milk, and sugar. Cook on griddle until golden. Top with butter and sprinkles.' },
    { mood: 'happy', name: 'Sunny Lemonade', ingredients: 'Lemons, Sugar, Water, Ice, Mint', instructions: 'Squeeze lemons, mix with sugar and water. Add ice and garnish with mint leaves.' },
    
    // Sad recipes (comfort food)
    { mood: 'sad', name: 'Mac and Cheese', ingredients: 'Pasta, Cheddar cheese, Milk, Butter, Salt', instructions: 'Cook pasta. Make cheese sauce with butter, milk, and cheese. Mix together and bake until bubbly.' },
    { mood: 'sad', name: 'Hot Chocolate', ingredients: 'Cocoa powder, Milk, Sugar, Vanilla, Marshmallows', instructions: 'Heat milk with cocoa and sugar. Add vanilla. Top with marshmallows.' },
    { mood: 'sad', name: 'Chicken Noodle Soup', ingredients: 'Chicken, Noodles, Carrots, Celery, Chicken broth', instructions: 'Boil chicken and vegetables in broth. Add noodles and simmer until tender.' },
    
    // Stressed recipes (calming)
    { mood: 'stressed', name: 'Chamomile Tea with Honey', ingredients: 'Chamomile tea bags, Honey, Lemon, Hot water', instructions: 'Steep tea in hot water for 5 minutes. Add honey and lemon to taste.' },
    { mood: 'stressed', name: 'Avocado Toast', ingredients: 'Bread, Avocado, Lemon, Salt, Pepper, Olive oil', instructions: 'Toast bread. Mash avocado with lemon, salt, and pepper. Spread on toast and drizzle with olive oil.' },
    { mood: 'stressed', name: 'Berry Smoothie', ingredients: 'Mixed berries, Banana, Yogurt, Honey, Spinach', instructions: 'Blend all ingredients until smooth. Serve immediately.' },
    
    // Energetic recipes
    { mood: 'energetic', name: 'Protein Power Bowl', ingredients: 'Quinoa, Grilled chicken, Avocado, Chickpeas, Tahini', instructions: 'Cook quinoa. Top with grilled chicken, avocado, and chickpeas. Drizzle with tahini.' },
    { mood: 'energetic', name: 'Energy Balls', ingredients: 'Oats, Peanut butter, Honey, Chocolate chips, Chia seeds', instructions: 'Mix all ingredients. Roll into balls. Refrigerate for 30 minutes.' },
    { mood: 'energetic', name: 'Green Juice', ingredients: 'Spinach, Cucumber, Apple, Lemon, Ginger', instructions: 'Blend all ingredients with water. Strain if desired. Drink fresh.' },
    
    // Relaxed recipes
    { mood: 'relaxed', name: 'Caprese Salad', ingredients: 'Tomatoes, Mozzarella, Basil, Olive oil, Balsamic vinegar', instructions: 'Slice tomatoes and mozzarella. Layer with basil. Drizzle with oil and vinegar.' },
    { mood: 'relaxed', name: 'Bruschetta', ingredients: 'Baguette, Tomatoes, Garlic, Basil, Olive oil', instructions: 'Toast bread slices. Top with diced tomatoes, garlic, and basil mixed with olive oil.' },
    { mood: 'relaxed', name: 'Iced Green Tea', ingredients: 'Green tea bags, Water, Honey, Lemon, Ice', instructions: 'Brew tea and let cool. Add honey and lemon. Serve over ice.' }
  ];

  const stmt = db.prepare('INSERT INTO recipes (mood, name, ingredients, instructions) VALUES (?, ?, ?, ?)');
  recipes.forEach(recipe => {
    stmt.run(recipe.mood, recipe.name, recipe.ingredients, recipe.instructions);
  });
  stmt.finalize();

  console.log('Database seeded successfully!');
});

db.close();
