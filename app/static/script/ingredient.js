function removeIngredient(removeIcon) {
    var ingredient = removeIcon.parentNode.parentNode;
    var ingredientList = document.getElementById("ingredients");
    ingredientList.removeChild(ingredient);

    var ingredientNames = document.getElementsByClassName("ingredient-name-input");
    var ingredientQuantities = document.getElementsByClassName("ingredient-quantity-input");
    var ingredientUnits = document.getElementsByClassName("ingredient-unit-input");

    for (let i = 0; i < ingredientNames.length; i++) {
        ingredientNames[i].setAttribute("name", `ingredient-name${i}`)
        ingredientQuantities[i].setAttribute("name", `quantity${i}`)
        ingredientUnits[i].setAttribute("name", `unit${i}`)
    }
}

function countIngredients() {
    var ingredientList = document.getElementById("ingredients").children;
    if (ingredientList.length === 0) {
        event.preventDefault();
        return alert("You are missing ingredients!");
    }
    var hiddenInput = document.getElementById("ingredient-count");
    hiddenInput.value = ingredientList.length;
}

function addIngredient() {
    var container = document.getElementById("ingredients");
    var ingredientDiv = document.createElement("div");
    ingredientDiv.classList.add("ingredient");
    var ct = container.children.length;

    ingredientDiv.innerHTML = `
    <div>
        <label for="ingredient_name">Name</label>
        <input type="text" class="ingredient-name-input" name="ingredient-name${ct}" class="form-control" required>
    </div>
    <div>
        <label for="quantity">Quantity</label>
        <input type="number" class="ingredient-quantity-input" name="quantity${ct}" min="0" class="form-control" step="any" required>
    </div>
    <div id="select-unit">
        <label for="unit" style="margin-top: -10px;">Unit</label>
        <select type="text" class="ingredient-unit-input" name="unit${ct}" class="form-control" required>
          <option value="count">count</option>
          <option value="tsp">tsp</option>
          <option value="tbsp">tbsp</option>
          <option value="fl oz">fl oz</option>
          <option value="cup">cups</option>
          <option value="pt">pt</option>
          <option value="qt">qt</option>
          <option value="gal">gal</option>
          <option value="pinch">pinch</option>
          <option value="mL">mL</option>
          <option value="L">L</option>
          <option value="mg">mg</option>
          <option value="g">g</option>
          <option value="kg">kg</option>
          <option value="lbs">lbs</option>
          <option value="oz">oz</option>
          <option value="sprigs">sprigs</option>
          <option value="cans">cans</option>
        </select>
    </div>
    <div>
        <img src="../../../static/img/red-x.png" alt="remove" class="remove-icon" id="remove-icon"
        onclick="removeIngredient(this)">
    </div>
    <input type="hidden" id="ingredient-count" name="ingredient-count" value="0">
    `;
    container.appendChild(ingredientDiv);
}