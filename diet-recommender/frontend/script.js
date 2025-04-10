document.getElementById('dietForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="flex justify-center items-center py-8">
            <i class="fas fa-spinner fa-spin text-blue-500 text-2xl mr-2"></i>
            <span class="text-gray-600">Generating your personalized diet plan...</span>
        </div>
    `;

    try {
        // Get form data
        const formData = {
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            height: document.getElementById('height').value,
            weight: document.getElementById('weight').value,
            activity_level: document.getElementById('activity').value,
            health_conditions: document.getElementById('health').value,
            dietary_restrictions: document.getElementById('diet').value,
            goal: document.getElementById('goal').value
        };

        // Call API
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        // Display results
        resultsDiv.innerHTML = `
            <div class="space-y-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                    <h3 class="font-medium text-blue-800 mb-2">
                        <i class="fas fa-fire mr-2"></i>Calorie Needs
                    </h3>
                    <p class="text-gray-700">Your estimated daily calorie needs: <span class="font-semibold">${data.daily_calories} kcal</span></p>
                    <p class="text-gray-700">Recommended daily intake for your goal: <span class="font-semibold">${data.recommended_calories} kcal</span></p>
                </div>

                <div class="bg-green-50 p-4 rounded-lg">
                    <h3 class="font-medium text-green-800 mb-2">
                        <i class="fas fa-utensils mr-2"></i>Meal Plan
                    </h3>
                    <p class="text-gray-700">${data.meal_plan}</p>
                </div>

                <div class="bg-purple-50 p-4 rounded-lg">
                    <h3 class="font-medium text-purple-800 mb-2">
                        <i class="fas fa-chart-pie mr-2"></i>Macronutrients
                    </h3>
                    <div class="grid grid-cols-3 gap-2 text-center">
                        <div class="bg-white p-2 rounded">
                            <p class="text-sm text-gray-500">Protein</p>
                            <p class="font-semibold">${data.macronutrients.protein}g</p>
                        </div>
                        <div class="bg-white p-2 rounded">
                            <p class="text-sm text-gray-500">Carbs</p>
                            <p class="font-semibold">${data.macronutrients.carbs}g</p>
                        </div>
                        <div class="bg-white p-2 rounded">
                            <p class="text-sm text-gray-500">Fat</p>
                            <p class="font-semibold">${data.macronutrients.fat}g</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="bg-red-50 p-4 rounded-lg text-red-600">
                <i class="fas fa-exclamation-circle mr-2"></i>
                Error generating recommendations. Please try again.
            </div>
        `;
        console.error('Error:', error);
    }
});
