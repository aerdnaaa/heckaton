import { StyleSheet, Text, View } from 'react-native';
import { CiShoppingCart } from "react-icons/ci";
import IngredientItem from './IngredientItem';

import React from 'react'
import { IngredientListProps } from './IngredientProps';

const IngredientComponent = ({ ingredients }: IngredientListProps) => {
    if (!ingredients?.length) {
        return;
    }
    return (
        <View style={styles.ingredientContainer}>
            <Text style={styles.mediumFont}><CiShoppingCart style={styles.icon} />Ingredient Lists</Text>
            <View>
                {ingredients.map(({ item, qty, unit }) => {
                    return <IngredientItem item={item} qty={qty} unit={unit} />
                })}

            </View>
        </View>
    )
}

export default IngredientComponent

const styles = StyleSheet.create({
    icon: {
        paddingRight: 5,
    },
    mediumFont: {
        fontSize: 20,
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center'
    },
    ingredientContainer: {
        width: '48%'
    }
})