export interface IngredientListProps {
    ingredients: Ingredient[];
}

export interface Ingredient {
    item: string;
    qty: number;
    unit: string;
}