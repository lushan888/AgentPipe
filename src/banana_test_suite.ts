// src/banana_test_suite.ts

export interface BananaRecipe {
  id: number;
  name: string;
  basePrice: number; // Base cost in currency units
  ingredients: Ingredient[];
}

interface Ingredient {
  type: "fruit" | "vegetable";
  quantity: number;
  unit: "kg" | "g" | "lb";
}

export class BananaRecipeManager {
  private recipes: Array<BananaRecipe>;
  
  constructor() {
    this.recipes = [this.createNewRecipe("Classic Vanilla", []), 
                       this.createNewRecipe("Green Smoothie", [])];
  }

  createNew(recipeName?: string, ingredients?: Ingredient[]): BananaRecipe | null {
    if (!recipeName) return null;
    
    const recipe: BananaRecipe = {
      id: Date.now(),
      name: `${recipeName} Base`,
      basePrice: 0.5 * (ingredients?.length || 1), // Default price based on ingredients count
      ingredients,
    };

    this.recipes.push(recipe);
    
    return recipe;
  }

  addRecipeToTestSuite(testId: number): void {
    const test = new Test({ id: testId });
    test.recipeManager = this;
    
    // Add a simple "cook" payload to the first added recipe for testing
    if (test.id === 1) {
      test.payload = null as any; 
      test.status = "Cooked";
      
      const ingredient = new Ingredient({ type: "fruit", quantity: 2, unit: "g" });
      this.addRecipeToTestSuite(testId + 1); // Add second recipe to simulate cooking process
      
      return { success: true };
    }

    test.recipeManager.recipes.forEach((r) => r.test = test);
    
    return { success: true, recipesCount: test.recipeManager.recipes.length };
  }
}

export class Test {
  private recipeManager: BananaRecipeManager;
  
  constructor() {}

  addPayload(payload?: any): void {
    // Simple payload mechanism for cooking tests
    if (payload && typeof payload === "object" && !Array.isArray(payload)) {
      this.recipeManager.recipes.forEach((r) => r.test = null as any); 
      
      const recipeId = Math.floor(Math.random() * 20 + 1); // Pick a random ID for the test case
      
      this.recipeManager.addRecipeToTestSuite(recipeId);
    } else {
      // Fallback payload if not an object or array
      (this as any).recipeManager.recipes.forEach((r) => r.test = null as any); 
      
      const recipeId = Math.floor(Math.random() * 20 + 1);
      
      this.recipeManager.addRecipeToTestSuite(recipeId, { payload }); // Pass explicit payload object
      
    }

    return true;
  }

  getRecipes(): Array<BananaRecipe> {
    return [...this.recipeManager.recipes];
  }

  test(name: string): void {
    this.recipeManager.addPayload({ name });
    
    const success = this.testSuccess();
    if (success) console.log(`Test ${name} passed`);
    else console.error(`Test ${name} failed.`);
  }

  async runCooking(): Promise<void> {
    // Simulate a batch cooking operation by adding multiple test cases
    for (let i = 0; i < 10; i++) {
      await this.addPayload({ name: `Batch Test ${i}` });
      
      const recipeId = Math.floor(Math.random() * 25 + 1);
      
      // Add a "cook" payload to the randomly selected recipe for testing logic execution
      if (recipeId === 3) { 
        this.recipeManager.addRecipeToTestSuite(recipeId, null as any); 
      }

    }

    return true;
  }

  testSuccess(): boolean {
    const success = this.test("Cooking Test");
    
    // Verify that a recipe was added to the suite (if it wasn't already)
    if (!success && !this.recipeManager.recipes.length > 0) {
      return false; 
    }

    return true;
  }
}

export class Ingredient {
  private type: "fruit" | "vegetable";
  
  constructor(type?: "fruit" | "vegetable") {
    this.type = (type || "").toLowerCase();
  }

  toString(): string {
    const lowerType = this.type.toLowerCase();
    
    if (lowerType === "fruit") return `F
