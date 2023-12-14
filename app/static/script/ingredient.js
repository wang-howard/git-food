function addIngredient() {
    var container = document.getElementById("ingredients");
    var ingredientDiv = document.createElement("div");
    ingredientDiv.classList.add("ingredient");

    ingredientDiv.innerHTML = `
    <div>
        <label for="ingredient_name">Name</label>
        <input type="text" name="ingredient_name" class="form-control" required>
    </div>
    <div>
        <label for="quantity">Quantity</label>
        <input type="number" name="quantity" min="0" class="form-control" required>
    </div>
    <div id="select-unit">
        <label for="unit" style="margin-top: -10px;">Unit</label>
        <select type="text" name="unit" class="form-control" required>
            <option value="tsp">tsp</option>
            <option value="tbsp">tbsp</option>
            <option value="fl oz">fl oz</option>
            <option value="cup">cup</option>
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
            <option value="sprig">sprig</option>
            <option value="count">count</option>
        </select>
    </div>
    <div>
        <img src="../static/img/red-x.png" alt="remove" class="remove-icon" id="remove-icon"
        onclick="removeIngredient(this)">
    </div>
    `;
    container.appendChild(ingredientDiv);
}

function removeIngredient(removeIcon) {
    parentIngredient = removeIcon.parentNode.parentNode
    ingredientList = document.getElementById("ingredients")
    ingredientList.removeChild(parentIngredient)
}