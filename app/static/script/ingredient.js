function removeIngredient(removeIcon) {
    parentIngredient = removeIcon.parentNode.parentNode
    ingredientList = document.getElementById('ingredients')
    ingredientList.removeChild(parentIngredient)
}

function countIngredients() {
    var ingredientList = document.getElementById("ingredients").children
    if (ingredientList.length === 0) {
        event.preventDefault()
        return alert('You are missing ingredients!')
    }
    var hiddenInput = document.getElementById("ingredient-count")
    hiddenInput.value = ingredientList.length
}