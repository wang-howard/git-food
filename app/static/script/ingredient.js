function addIngredient() {
    var container = document.getElementById("ingredients");
    var ingredientDiv = document.createElement("div");
    ingredientDiv.classList.add("ingredient");

    ingredientDiv.innerHTML = `
        <label for="ingredient_name">Name:</label>
        <input type="text" name="ingredient_name[]" required>

        <label for="quantity">Quantity:</label>
        <input type="number" name="quantity[]" min="0" required>

        <label for="unit">Unit:</label>
        <input type="text" name="unit[]" required>
    `;
    container.appendChild(ingredientDiv);
}