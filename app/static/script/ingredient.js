function removeIngredient(removeIcon) {
    parentIngredient = removeIcon.parentNode.parentNode
    ingredientList = document.getElementById('ingredients')
    ingredientList.removeChild(parentIngredient)
}

function countIngredients() {
    var ingredientList = document.getElementById("ingredients").children
    var hiddenInput = document.getElementById("ingredient-count")
    hiddenInput.value = ingredientList.length
}