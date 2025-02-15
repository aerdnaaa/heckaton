import { StyleSheet, Text, View } from 'react-native'
import { FaRegCircle } from "react-icons/fa";
import React from 'react'
import { Ingredient } from './IngredientProps';

const IngredientItem = ({ item, qty, unit }: Ingredient) => {
    return (
        <View style={styles.ingredientItem}>
            <FaRegCircle style={styles.icon} />
            <Text style={styles.item}>{item}</Text>
            <View style={styles.measuring}>
                <Text>{qty}</Text>
                <Text>{unit}</Text>
            </View>
        </View>
    )
}

export default IngredientItem

const styles = StyleSheet.create({
    icon: {
        paddingRight: 5,
    },
    item: {
        width: '70%',
    },

    measuring: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '15%'
    },
    ingredientItem: {
        paddingTop: 10,
        display: 'flex',
        flexDirection: 'row',
    }
})